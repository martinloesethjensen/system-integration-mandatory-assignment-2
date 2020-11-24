using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace BankSystem.Models
{
    public class BankUserDto
    {
        [Key]
        [Column("Id")]
        [Required]
        [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
        public virtual int Id { get; set; }
        
        [Column("UserrId")]
        [Required]
        public virtual int UserId { get; set; }

        [Column("CreatedAt")]
        [Required]
        public virtual long CreatedAt { get; set; }

        [Column("ModifiedAt")]
        [Required]
        public virtual long ModifiedAt { get; set; }
    }
}
