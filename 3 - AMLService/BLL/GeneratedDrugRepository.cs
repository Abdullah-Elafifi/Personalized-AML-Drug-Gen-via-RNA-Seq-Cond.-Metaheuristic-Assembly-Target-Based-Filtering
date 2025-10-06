using AMLService.Models;

namespace AMLService;

public class GeneratedDrugRepository : IGeneratedDrugRepository
{
    private readonly AmlDbContext _context;

    public GeneratedDrugRepository(AmlDbContext context)
    {
        _context = context;
    }

    public void Insert(GeneratedDrug drug)
    {
        _context.GeneratedDrugs.Add(drug);
        _context.SaveChanges();
    }

    public void Delete(int id)
    {
        var x = _context.GeneratedDrugs.Find(id);
        if (x is not null)
            _context.GeneratedDrugs.Remove(x);
        _context.SaveChanges();
    }

    public GeneratedDrug? Get(int id)
    {
        return _context.GeneratedDrugs.Find(id);
    }
}