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
                        var result = await connection.QueryFirstOrDefaultAsync("select UserId from BankUser where Id = @Id", new { Id = bodyPayload.UserId }, transaction);
                        var withdrawMoneyresult = await connection.ExecuteAsync
                        (
                            @"
                            DECLARE @amount INT
                            SELECT 
                                @amount = Amount
                            FROM	
                                Account WHERE BankUserId = @BankUserId 
                            IF @amount > 0  and @amount > @substract
                            UPDATE 
                                Account SET Amount = @amount - @substract WHERE BankUserId = @BankUserId", new { BankUserId = result.UserId, substract = bodyPayload.Amount } , transaction
                        );
                        if (withdrawMoneyresult != 1) new Exception(); // Change to custom exception
                        transaction.Commit();
                        return Ok();
                    }
                    catch (Exception ex)
                    {
                        transaction.Rollback();
                        return NotFound("Withdrawal failed.");
                    }
                }
            }
        }
    }
}
