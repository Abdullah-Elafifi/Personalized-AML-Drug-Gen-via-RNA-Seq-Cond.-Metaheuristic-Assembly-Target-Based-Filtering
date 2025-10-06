using System.Text.Json.Serialization;

namespace AMLService.Models;

public class GeneratedDrug
{
    public int GeneratedDrugID { get; set; }
    public byte[] ProteinStructure { get; set; }
    public string CompletionDate { get; set; }
    
    // Analysis Foreign RelationShip
    public int AnalysisID { get; set; }
    [JsonIgnore]
    public Analysis Analysis { get; set; }
    // Other Metrics To Be Added ...
}