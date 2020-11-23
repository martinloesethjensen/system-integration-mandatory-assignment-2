using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace BankSystem.Models
{
    public class AccountDto
    {
        [Key]
        [Required]
        [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
        [Column("Id")]
        public virtual int Id { get; set; }

        [Required]
        [Column("BankUserId")]
        [ForeignKey("Id")]
        public virtual int BankUserId { get; set; }

        [Required]
        
        [Column("AccountNo")]
        public virtual int AccountNo { get; set; }

        [Required]
        [Column("IsSudent")]
        public virtual bool IsStudent { get; set; }

        [Required]
        [Column("CreatedAt")]
        public virtual long CreatedAt { get; set; }

        [Required]
        [Column("ModifiedAt")]
        public virtual long ModifiedAt { get; set; }

        [Required]
        [Column("Amount")]
        public virtual double Amount { get; set; }
    }
}
