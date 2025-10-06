using System.Security.Claims;
using AMLService.Uploaded;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace AMLService;

[ApiController]
[Route("api/[controller]")]
public class AMLController : Controller
{
    private readonly IAnalysisRepository _analysisRepository;
    private readonly RabbitMqService _rabbitMqService;

    public AMLController(IAnalysisRepository repository, RabbitMqService rabbitMqService)
    {
        this._analysisRepository = repository;
        this._rabbitMqService = rabbitMqService;
    }

    #region HelperFunctions

    private async Task<IActionResult?> HandleAMlRequest(AMLUserRequest? request)
    {
        if (request == null || request.CSVFile == null)
        {
            return BadRequest("CSV File Is Required");
        }

        string userId = User.Claims.First(c => c.Type == ClaimTypes.NameIdentifier).Value;
        var analysis = new Analysis()
        {
            UserID = userId,
            CreationDate = DateTime.Now,
        };
        // Convert file to byte array
        byte[] fileBytes;
        using (var ms = new MemoryStream())
        {
            await request.CSVFile.CopyToAsync(ms);
            fileBytes = ms.ToArray();
        }

        _analysisRepository.Insert(analysis);
        // Prepare message
        var message = new
        {
            FileName = request.CSVFile.FileName,
            FileData = Convert.ToBase64String(fileBytes),
            UserId = userId,
            AnalysisID = analysis.AnalysisID
        };

        // Send to RabbitMQ
        _rabbitMqService.Publish("aml.requests", message);

        return null;
    }

    private IActionResult? CheckAuthority(string userId)
    {
        // Extract the 'sub' claim from the JWT
        var userIdClaim = User.Claims.FirstOrDefault(c => c.Type == ClaimTypes.NameIdentifier);

        if (userIdClaim == null)
        {
            return Unauthorized("No user identifier found in token.");
        }

        if (userIdClaim.Value.Length == 0)
        {
            return Unauthorized("Invalid user identifier in token.");
        }

        // Compare token sub (user ID) with the requested id
        var userIdFromToken = userIdClaim.Value;
        if (userIdFromToken != userId)
        {
            return StatusCode(StatusCodes.Status403Forbidden, new
            {
                Message = "You are not allowed to access this resource."
            });
        }

        return null;
    }

    #endregion

    [Authorize(Roles = "User,Admin")]
    [HttpPost("upload")]
    public async Task<IActionResult> Submit([FromForm] AMLUserRequest? request)
    {
        var x = await HandleAMlRequest(request);
        if (x != null) return x;
        var response = new AMLUserResponse()
        {
            StatusCode = 200,
            Message = "File has been sent to processing queue",
        };

        return Ok(response);
    }


    [Authorize(Roles = "User,Admin")]
    [HttpGet("getPendingAnalysis")]
    public IActionResult GetPendingAnalysis()
    {
        var userId = User.Claims.First(c => c.Type == ClaimTypes.NameIdentifier).Value;
        /*var authority = CheckAuthority(userId);
        if (authority != null) return authority;*/

        // Proceed with your logic to get analysis from DB
        var analysis = _analysisRepository.GetPendingByUserId(userId);
        return Ok(analysis);
    }

    [Authorize(Roles = "User,Admin")]
    [HttpGet("getCompletedAnalysis")]
    public IActionResult GetCompletedAnalysis()
    {
        /*var authority = CheckAuthority(userId);
        if (authority != null) return authority;*/
        var userId = User.Claims.First(c => c.Type == ClaimTypes.NameIdentifier).Value;

        // Proceed with your logic to get analysis from DB
        var analysis = _analysisRepository.GetCompletedByUserId(userId);
        return Ok(analysis);
    }
}