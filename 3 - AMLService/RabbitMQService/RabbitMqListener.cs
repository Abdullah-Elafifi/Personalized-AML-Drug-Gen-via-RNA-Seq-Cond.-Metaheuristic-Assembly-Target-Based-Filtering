using System.Text.Json;
using AMLService;
using AMLService.Models;
using AMLService.Uploaded;
using Microsoft.Extensions.DependencyInjection;

public class RabbitMqListener : BackgroundService
{
    private readonly RabbitMqService _rabbitMqService;
    private readonly IServiceProvider _serviceProvider;

    public RabbitMqListener(RabbitMqService rabbitMqService, IServiceProvider serviceProvider)
    {
        _rabbitMqService = rabbitMqService;
        _serviceProvider = serviceProvider;
    }

    protected override Task ExecuteAsync(CancellationToken stoppingToken)
    {
        _rabbitMqService.Consume("aml.responses", (message) =>
        {
            Console.WriteLine($"📩 Received Response: {message}");

            // Deserialize incoming JSON
            var result = JsonSerializer.Deserialize<GeneratedDrug>(message, new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            });
            if (result == null)
            {
                Console.WriteLine("⚠️ Failed to deserialize message.");
                return;
            }

            // Create scope to resolve scoped services (repositories)
            using var scope = _serviceProvider.CreateScope();
            var analysisRepository = scope.ServiceProvider.GetRequiredService<IAnalysisRepository>();
            var drugRepository = scope.ServiceProvider.GetRequiredService<IGeneratedDrugRepository>();

            // Mark the analysis as completed
            analysisRepository.MarkAsCompleted(result.AnalysisID);

            // Insert the generated drug
            drugRepository.Insert(result);

            Console.WriteLine($"✅ Analysis {result.AnalysisID} marked completed, drug saved.");
        });

        return Task.CompletedTask;
    }
}