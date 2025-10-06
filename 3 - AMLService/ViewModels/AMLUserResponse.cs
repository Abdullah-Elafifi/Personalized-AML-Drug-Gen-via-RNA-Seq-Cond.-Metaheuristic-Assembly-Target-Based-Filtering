namespace AMLService;

public class AMLUserResponse
{
    public IFormFile AllRankedBiomarkers { get; set; }
    public IFormFile ExpressionSummary { get; set; }
    public IFormFile HVGSSummary { get; set; }
    public IFormFile ModuleEigenGenes { get; set; }
    public IFormFile ProtienStructureReport { get; set; }
    
    
    // After Analysis
    public IFormFile TopBiomarkersCSV { get; set; }
    public IFormFile TopBiomarkersEDA { get; set; }
    public IFormFile TopProtienStructurePDBFormat { get; set; }
    public IFormFile TopProtienStructurePNGFormat { get; set; }
    public IFormFile CollageForTopProtiens { get; set; }
    public IFormFile StructureProtienReport { get; set; }
    public IFormFile GeneExpressionCSV { get; set; }
    public IFormFile GeneExpressionProtienCoding { get; set; }
}