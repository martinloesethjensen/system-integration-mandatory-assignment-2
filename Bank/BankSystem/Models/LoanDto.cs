using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace BankSystem.Models
{
    public class LoanDto
    {
        public LoanDto()
        {

        }

        public LoanDto(int bankUserId, long modifiedAt, double amount)
        {
            BankUserId = bankUserId;
            ModifiedAt = modifiedAt;
            Amount = amount;
        }

        public LoanDto(int bankUserId, long createdAt, long modifiedAt, double amount)
        {
            BankUserId = bankUserId;
            CreatedAt = createdAt;
            ModifiedAt = modifiedAt;
            Amount = amount;
        }

        [Key]
        [Column("Id")]
        [Required]
        [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
        public int Id { get; set; }

        [ForeignKey("Id")]
        [Required]
        [Column("BankUserId")]
        public int BankUserId { get; set; }
        
        [Required]
        [Column("CreatedAt")]
        public long CreatedAt { get; set; }

        [Required]
        [Column("ModifiedAt")]
        public long ModifiedAt { get; set; }

        [Required]
        [Column("Amount")]
        public double Amount { get; set; }
    }
}
