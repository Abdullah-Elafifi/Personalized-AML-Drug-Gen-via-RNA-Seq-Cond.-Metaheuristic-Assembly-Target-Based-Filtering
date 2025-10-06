using System.Net.Mime;

namespace AMLService;

public abstract class AMLUserRequest
{
    public int NumberOfBioMarkers { get; set; }
    public bool EDA { get; set; } = true;
    public string Normalization { get; set; } = "null";
}

public class AMLRawUserRequest : AMLUserRequest
{
    public IFormFile RawData { get; set; }
    public IFormFile ExonData { get; set; } // Annotation Data
}

public class AMLMappedUserRequest : AMLUserRequest
{
    public IFormFile FullGeneExpression { get; set; }
}