using System.Threading.Tasks;
using BankSystem.Interfaces;
using BankSystem.Models;
using BankSystem.Utils;
using Dapper;
using Microsoft.AspNetCore.Mvc;

namespace BankSystem.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class BankUsersController : ControllerBase
    {
        private readonly IDatabaseStrategy _databaseContext;

        public BankUsersController(IDatabaseStrategy databaseContext)
        {
            _databaseContext = databaseContext;
        }

        // GET: api/<BankUsersController>
        [HttpGet]
        public async Task<IActionResult> GetAllBankUsers()
        {
            using (var connection = _databaseContext.Connection)
            {
                var data = await connection.QueryAsync<BankUserDto>("select * from BankUser");
                if (data != null) return Ok(data);
                else return NotFound();
            }
        }

        // GET api/<BankUsersController>/5
        [HttpGet("{id}")]
        public async Task<IActionResult> GetBankUserById(int id)
        {
            using (var connection = _databaseContext.Connection)
            {
                var data = await connection.QueryFirstOrDefaultAsync<BankUserDto>("select * from BankUser where Id = @Id", new { Id = id});
                if (data != null) return Ok(data);
                else return NotFound();
            }
        }

        // POST api/<BankUsersController>
        [HttpPost]
        public async Task<IActionResult> CreateBankUser([FromBody] BankUserDto bodyInput)
        {
            long timeStamp = TimeStamp.GetDateTimeOffsetNowAsUnixTimeStampInSeconds();

            bodyInput.CreatedAt = timeStamp;
            bodyInput.ModifiedAt = timeStamp;

            using (var connection = _databaseContext.Connection)
            {
                var result = await connection.ExecuteAsync(@"insert into BankUser (UserId, CreatedAt, ModifiedAt) values (@UserId, @CreatedAt, @ModifiedAt )", bodyInput);
                if (result == 1) return Ok();
                else return NotFound();
            }
        }

        // PUT api/<BankUsersController>/5
        [HttpPut()]
        public async Task<IActionResult> UpdateBankUser([FromBody] BankUserDto bodyPayload)
        {
            /* TODO
            * Update FK refererences too
            * Transaction 
            */

            long timeStamp = TimeStamp.GetDateTimeOffsetNowAsUnixTimeStampInSeconds();
            bodyPayload.ModifiedAt = timeStamp;

            using (var connection = _databaseContext.Connection)
            {
                var result = await connection.ExecuteAsync(@"update BankUser set UserId = @UserId, ModifiedAt = @ModifiedAt where Id = @Id ", bodyPayload);
                if (result == 1) return Ok();
                else return NotFound();
            }
        }

        // DELETE api/<BankUsersController>/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteBankUser(int id)
        {
            using (var connection = _databaseContext.Connection)
            {
                var result = await connection.ExecuteAsync("delete from BankUser where Id = @Id", new{ Id = id });
                if (result == 1) return Ok();
                else return NotFound();
            }
        }
    }
}
