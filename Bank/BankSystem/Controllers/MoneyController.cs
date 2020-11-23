using System;
using System.Threading.Tasks;
using BankSystem.Interfaces;
using BankSystem.Models;
using Dapper;
using Microsoft.AspNetCore.Mvc;

namespace BankSystem.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class MoneyController : ControllerBase
    {
        private readonly IDatabaseStrategy _databaseContext;

        public MoneyController(IDatabaseStrategy databaseConext)
        {
            _databaseContext = databaseConext;
        }

        // POST api/<MoneyController>
        [HttpPost("withdrawl")]
        public async Task<IActionResult> WithdrawlMoney([FromBody] MoneyRequest bodyPayload)
        {
            /*
             * The body of that request should contain an amount and a UserId(Not BankUserId, not SkatUserId)
             * Subtract (if possible) the amount from that users account. Throw an error otherwise.
             */

            if (bodyPayload.Amount <= 0) return Conflict("Amount cannot be 0 or negative.");

            using (var connection = _databaseContext.Connection)
            {
                using (var transaction = connection.BeginTransaction())
                {
                    try
                    {
                        var bankUserId = await connection.QueryFirstOrDefaultAsync("select UserId from BankUser where Id = @Id", new { Id = bodyPayload.UserId });
                        var withdrawMoneyresult = await connection.ExecuteAsync
                        (
                            @"
                            DECLARE @amount BIGINT
                            SELECT 
                                @amount = Amount
                            FROM	
                                Account WHERE BankUserId = @BankUserId 
                            IF @amount > 0
                            UPDATE 
                                Account SET Amount = 8000 WHERE BankUserId = @BankUserId", new { BankUserId = bankUserId }
                        );
                        if (withdrawMoneyresult != 1) new Exception(); // Change to custom exception
                        transaction.Commit();
                        return Ok();
                    }
                    catch (Exception)
                    {
                        transaction.Rollback();
                        return NotFound("Withdrawal failed.");
                    }
                }
            }
        }
    }
}
