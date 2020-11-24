using System.Data.Common;

namespace BankSystem.Interfaces
{
    public interface IDatabaseStrategy
    {
        void SeedDatabase();
        DbConnection Connection { get; }
    }
}
