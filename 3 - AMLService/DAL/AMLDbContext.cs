using AMLService.Models;
using Microsoft.EntityFrameworkCore;

namespace AMLService;

public class AmlDbContext : DbContext
{
    public AmlDbContext(DbContextOptions<AmlDbContext> options) : base(options)
    {
    }


    public DbSet<Analysis> Analyses { get; set; }
    public DbSet<GeneratedDrug> GeneratedDrugs { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Analysis>(
            a =>
            {
                a.HasKey(k => k.AnalysisID);
                a.Property(k => k.UserID).IsRequired();
                a.Property(k => k.Status).HasDefaultValue("Pending");
                a.HasOne(k => k.GeneratedDrug).WithOne(k => k.Analysis)
                    .HasForeignKey<GeneratedDrug>(g => g.AnalysisID).OnDelete(DeleteBehavior.Cascade); // FK lives in GeneratedDrug;
            }
        );
        
        modelBuilder.Entity<GeneratedDrug>(
            g =>
            {
                g.HasKey(e => e.GeneratedDrugID);
                g.Property(e => e.ProteinStructure).IsRequired(false);
                g.HasOne(e => e.Analysis).WithOne(e => e.GeneratedDrug);
            }
        );
    }
}