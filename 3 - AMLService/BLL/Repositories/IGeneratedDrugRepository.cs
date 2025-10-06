using AMLService.Models;

namespace AMLService;

public interface IGeneratedDrugRepository
{
    public void Insert(GeneratedDrug analysis);
    //public void Update(GeneratedDrug analysis);
    public void Delete(int id);
    public GeneratedDrug? Get(int id);
}