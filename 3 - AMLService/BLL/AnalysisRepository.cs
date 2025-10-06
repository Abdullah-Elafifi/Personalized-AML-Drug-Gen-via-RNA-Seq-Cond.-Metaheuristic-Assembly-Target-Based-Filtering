using Microsoft.EntityFrameworkCore;

namespace AMLService;

public class AnalysisRepository : IAnalysisRepository
{
    private readonly AmlDbContext _context;

    public AnalysisRepository(AmlDbContext context)
    {
        this._context = context;
    }

    public void MarkAsCompleted(int id)
    {
        _context.Analyses.Find(id)!.Status = "Completed";
        _context.SaveChanges();
    }

    public void Insert(Analysis analysis)
    {
        _context.Add(analysis);
        _context.SaveChanges();
    }


    public void Delete(int id)
    {
        var x = Get(id);
        if (x != null)
            _context.Analyses.Remove(x);
    }

    public Analysis? Get(int id)
    {
        return _context.Analyses.Find(id);
    }

    public List<Analysis> GetCompletedByUserId(string userId)
    {
        return _context.Analyses
            .Where(a => a.UserID == userId)
            .Where(a => a.Status == "Completed")
            .Include(a => a.GeneratedDrug).ToList();
    }

    public List<Analysis> GetPendingByUserId(string userId)
    {
        return _context.Analyses.Where(a => a.UserID == userId).Where(a => a.Status == "Pending").ToList();
    }
}