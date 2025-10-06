namespace AMLService;

public interface IAnalysisRepository
{
    public void MarkAsCompleted(int id);

    public void Insert(Analysis analysis);

    //public void Update(Analysis analysis);
    public void Delete(int id);
    public Analysis? Get(int id);
    public List<Analysis> GetCompletedByUserId(string userId);
    public List<Analysis> GetPendingByUserId(string userId);
}