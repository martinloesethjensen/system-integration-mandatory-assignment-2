﻿using System.Threading.Tasks;
using BankSystem.Interfaces;
using BankSystem.Models;
using BankSystem.Utils;
using Dapper;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace BankSystem.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class AccountsController : ControllerBase
    {
        private readonly IDatabaseStrategy _databaseContext;

        public AccountsController(IDatabaseStrategy databaseContext)
        {
            _databaseContext = databaseContext;
        }

        // GET: api/<AccountsController>
        [HttpGet]
        public async Task<IActionResult> RetrieveAllAccounts()
        {
            using (var connection = _databaseContext.Connection)
            {
                var data = await connection.QueryAsync<AccountDto>("select * from Account");
                if (data == null) return NotFound("There are no accounts created yet.");
                return Ok(data);
            }
        }

        // GET api/<AccountsController>/5
        [HttpGet("{id}")]
        public async Task<IActionResult> RetrieveAccountById(int id)
        {
            using (var connection = _databaseContext.Connection)
            {
                var data = await connection.QueryFirstOrDefaultAsync<AccountDto>("select * from Account where Id = @Id ", new { Id = id });
                if (data == null) return NotFound($"Account does not exist on id:{id}");
                return Ok(data);
            }
        }

        // POST api/<AccountsController>
        [HttpPost]
        public async Task<IActionResult> CreateAccount([FromBody] AccountDto bodyPayload)
        {
            long timeStamp = TimeStamp.GetDateTimeOffsetNowAsUnixTimeStampInSeconds();

            bodyPayload.CreatedAt = timeStamp;
            bodyPayload.ModifiedAt = timeStamp;

            using (var connection = _databaseContext.Connection)
            {
                var result = await connection.ExecuteAsync("insert into Account (BankUserId,AccountNo,IsStudent,CreatedAt,ModifiedAt,Amount)" +
                                                           "values (@BankUserId,@AccountNo,@IsStudent,@CreatedAt,@ModifiedAt,@Amount)", bodyPayload);
                if (result != 1) return NotFound("Account could not be created.");
                return new ObjectResult("Account created.") { StatusCode = StatusCodes.Status204NoContent };
            }
        }

        // PUT api/<AccountsController>/5
        [HttpPut()]
        public async Task<IActionResult> UpdateAccount([FromBody] AccountDto bodyPayload)
        {
            long timeStamp = TimeStamp.GetDateTimeOffsetNowAsUnixTimeStampInSeconds();
            bodyPayload.ModifiedAt = timeStamp;

            using (var connection = _databaseContext.Connection)
            {
                var result = await connection.ExecuteAsync("update Account set BankUserId = @BankUserId, AccountNo = @AccountNo, " +
                                                            "IsStudent = @IsStudent, Amount = @Amount, ModifiedAt = @ModifiedAt", bodyPayload);

                if (result != 1) return NotFound("Account not found or could not be updated.");
                return new ObjectResult("Account updated.") { StatusCode = StatusCodes.Status204NoContent };
            }
        }

        // DELETE api/<AccountsController>/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteAccount(int id)
        {
            using (var connection = _databaseContext.Connection)
            {
                var result = await connection.ExecuteAsync("delete from Account where Id = @Id", new { Id = id });
                if (result == 1) return new ObjectResult("Account deleted.") { StatusCode = StatusCodes.Status204NoContent };
                else return NotFound($"Account doesn't exist on id:{id}.");
            }
        }
    }
}
