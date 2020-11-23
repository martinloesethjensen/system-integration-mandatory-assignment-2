namespace BankSystem.Models
{
    public class AccountRequest
    {     
        public virtual int BankUserId { get; set; }
        public virtual int AccountNo { get; set; }
        public virtual bool IsStudent { get; set; }
        public virtual double Amount { get; set; }
    }
}

