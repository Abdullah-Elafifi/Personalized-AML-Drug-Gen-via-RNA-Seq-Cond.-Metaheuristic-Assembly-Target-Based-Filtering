using AMLService.Models;

namespace AMLService;

public class Analysis
{
    public int AnalysisID { get; set; }
    public string UserID { get; set; }
    public DateTime CreationDate { get; set; }
    public string Status { get; set; }
    
    
    // Foreign Key and Navigational Property
    public GeneratedDrug GeneratedDrug { get; set; }
}