using System.Net.Mime;

namespace AMLService;

public class AMLUserRequest
{
    public IFormFile CSVFile { get; set; }
    // User Preferences To Be Added
    public string Preferences { get; set; }
}