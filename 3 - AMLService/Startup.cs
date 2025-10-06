using System.Security.Claims;
using System.Text;
using AMLService.Uploaded;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using Microsoft.OpenApi.Models;

namespace AMLService;

public class Startup
{
    IConfiguration _configuration;

    public Startup(IConfiguration configuration)
    {
        this._configuration = configuration;
    }

    public void ConfigureServices(IServiceCollection services)
    {
        services.AddControllers();
        // ✅ Add Swagger
        services.AddEndpointsApiExplorer();
        services.AddSwaggerGen(c =>
        {
            c.SwaggerDoc("v1", new OpenApiInfo
            {
                Title = "My API",
                Version = "v1"
            });

            // 🔑 Add JWT Auth
            c.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
            {
                Name = "Authorization",
                Type = SecuritySchemeType.ApiKey,
                Scheme = "Bearer",
                BearerFormat = "JWT",
                In = ParameterLocation.Header,
                Description =
                    "Enter 'Bearer' [space] and then your valid token.\nExample: \"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6...\""
            });

            c.AddSecurityRequirement(new OpenApiSecurityRequirement
            {
                {
                    new OpenApiSecurityScheme
                    {
                        Reference = new OpenApiReference
                        {
                            Type = ReferenceType.SecurityScheme,
                            Id = "Bearer"
                        }
                    },
                    new string[] { }
                }
            });
        });

        // Configure JWT Authentication
        services.AddAuthentication(options =>
            {
                options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
                options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
                options.DefaultScheme = JwtBearerDefaults.AuthenticationScheme;
            })
            .AddJwtBearer(options =>
            {
                var secretKey = _configuration["JwtSettings:SecretKey"];
                var issuer = _configuration["JwtSettings:Issuer"];
                var audience = _configuration["JwtSettings:Audience"];

                if (string.IsNullOrEmpty(secretKey) || secretKey.Length < 32)
                {
                    throw new InvalidOperationException("JWT SecretKey must be at least 32 characters long");
                }

                options.SaveToken = true;
                options.RequireHttpsMetadata = false;

                options.TokenValidationParameters = new TokenValidationParameters
                {
                    ValidateIssuerSigningKey = true,
                    IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(secretKey)),
                    ValidateIssuer = true,
                    ValidIssuer = issuer,
                    ValidateAudience = true,
                    ValidAudience = audience,
                    ValidateLifetime = true,
                    ClockSkew = TimeSpan.Zero,

                    // Critical: These settings handle claim mapping correctly
                    NameClaimType = ClaimTypes.Name,
                    RoleClaimType = ClaimTypes.Role,

                    // For .NET 7 compatibility
                    RequireExpirationTime = true,
                    RequireSignedTokens = true
                };
            });

        services.AddAuthorizationBuilder()
            .AddPolicy("User", policy => policy.RequireRole("User"))
            .AddPolicy("Admin", policy => policy.RequireRole("Admin"));

        services.AddDbContext<AmlDbContext>(
            options => { options.UseSqlServer(_configuration.GetConnectionString("DefaultConnection")); });

        services.AddScoped<IAnalysisRepository, AnalysisRepository>();
        services.AddScoped<IGeneratedDrugRepository, GeneratedDrugRepository>();

        services.AddSingleton(new RabbitMqService(
            hostName: _configuration["RabbitMQ:hostName"], // أو الـ IP بتاع RabbitMQ Server
            userName: _configuration["RabbitMQ:userName"],
            password: _configuration["RabbitMQ:password"]
        ));
        services.AddHostedService<RabbitMqListener>();
    }

    public async Task Configure(WebApplication app, IWebHostEnvironment env)
    {
        if (app.Environment.IsDevelopment())
        {
        }

        app.UseSwagger();
        app.UseSwaggerUI(c =>
        {
            c.SwaggerEndpoint("/swagger/v1/swagger.json", "My API V1");
            c.RoutePrefix = string.Empty; // Swagger UI يظهر على "/"
        });
        app.UseHttpsRedirection();
        app.UseAuthentication();
        app.UseAuthorization();
        app.MapControllers();
        // Apply Any Pending Migrations
        using var scope = app.Services.CreateScope();
        try
        {
            var services = scope.ServiceProvider;
            var context = services.GetRequiredService<AmlDbContext>();
            await context.Database.EnsureCreatedAsync(); // ensures DB exists
            await context.Database.MigrateAsync(); // applies migrations

            Console.WriteLine("Database initialization completed successfully.");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"An error occurred while initializing the database: {ex.Message}");
            // In production, you might want to log this properly
        }
    }
}