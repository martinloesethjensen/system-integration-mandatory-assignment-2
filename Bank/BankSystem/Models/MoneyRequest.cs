namespace BankSystem.Models
{
    public class MoneyRequest
    {
        public int UserId { get; set; } // Not equal to BankUserID !
        public double Amount { get; set; }
    }
}
