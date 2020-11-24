using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace BankSystem.Models
{
    public class DepositDto
    {
        public DepositDto()
        {
               
        }

        public DepositDto(int bankUserId, long createdAt, double amount)
        {
            BankUserId = bankUserId;
            CreatedAt = createdAt;
            Amount = amount;
        }

        [Key]
        [Required]
        [Column("Id")]
        [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
        public virtual int Id { get; set; }

        [ForeignKey("Id")]
        [Required]
        [Column("BankUserId")]
        public virtual int BankUserId { get; set; }

        [Required]
        [Column("CreatedAt")]
        public long CreatedAt { get; set; }

        [Required]
        [Column("Amount")]
        public double Amount { get; set; }
    }
}
