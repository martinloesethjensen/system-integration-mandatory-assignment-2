using System;
using System.Collections.Generic;
using System.Net;
using System.Threading;
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
    public class LoansController : ControllerBase
    {
        private readonly IDatabaseStrategy _databaseContext;

        public LoansController(IDatabaseStrategy databaseContext)
        {
            _databaseContext = databaseContext;
        }

        // POST api/<LoansController>
        [HttpPost("create-loan")]
        public async Task<IActionResult> CreateLoan([FromBody] LoanRequest bodyPayload)
        {
            /*
             * Request will contain the BankUserIdand LoanAmount. (/)
             * A POST request will be made to the Loan Algorithm Functionwith an amount and the total account amount for that user(/)
             * If the status code is 200, a loan record will be created (/)
             * If the status code is 403 or similar, an error will be returned (/)
             * The amount will be added to the Account of that user –if it is successfulof course. (/)
             */

            if (bodyPayload.LoanAmount <= 0) return Conflict("LoanAmount cannot be 0 or negative");

            using (var connection = _databaseContext.Connection)
            {
                using (var transaction = connection.BeginTransaction())
                {
                    try
                    {
                        var totalAmount = connection.QueryFirstOrDefaultAsync("select SUM(Amount) from Loan where BankUserId = @BankUserId", new { BakUserId = bodyPayload.BankUserId} );
                        if (totalAmount == null) return Conflict("Account could not be fetched");
                        var response = await HTTP.PostRequest("url", new { loanAmount = bodyPayload.LoanAmount, accountAmount = totalAmount }, CancellationToken.None); // URL is to be filled

                        if (response.StatusCode == HttpStatusCode.OK)
                        {
                            long timeStamp = TimeStamp.GetDateTimeOffsetNowAsUnixTimeStampInSeconds();
                            LoanDto loanDto = new LoanDto(bodyPayload.BankUserId, timeStamp, timeStamp, bodyPayload.LoanAmount);
                            var loanResult = await connection.ExecuteAsync("insert into Loan(BankUserId,CreatedAt,ModifiedAt,Amount)" +
                                                                        "values (@BankUserId,@CreatedAt,@ModifiedAt,@Amount)", timeStamp);
 
                            AccountDto accountDto = new AccountDto();
                            accountDto.Amount = bodyPayload.LoanAmount;
                            accountDto.ModifiedAt = timeStamp;
                            accountDto.BankUserId = bodyPayload.BankUserId;
                            var accountResult = await connection.ExecuteAsync("update Account set Amount = @Amount, ModifiedAt = @ModifiedAt where BankUserId = @BankUserId", bodyPayload );

                            if (loanResult != 1 && accountResult != 1) new Exception(); // Need be replaced with custom exception.
                        }
                        else return Conflict("This account is not eligible for further loans.");

                        transaction.Commit();
                        return Ok();
                    }
                    catch (Exception)
                    {
                        transaction.Rollback();
                        return NotFound("Loan could not be created");
                    }
                }
            }

        }


        // POST api/<LoansController>
        [HttpPost("pay-loan")]
        public async Task<IActionResult> PayLoad([FromBody] string value)
        {
            /*
             * The loan can be paid integrally by using the /pay-loan endpoint. 
             * The request will contain the BankUserId and the LoanId as well.
             * This will make the amountfrom a loan 0 and will subtract that amount from the accountof that user. 
             * If there aren’t enough money on the account, an error will be returned.
             */
            return Ok();
        }

        [HttpGet("list-loans/{userId}")]
        public async Task<IActionResult> ListLoans(int userId) 
        {
            /*
             * GET request which will return a list of all the loans belonging to a user that are greater than 0 (not paid) (/)
             * The request should have a BankUserId to retrieve the loans for a user (/)
             */

            using (var connection = _databaseContext.Connection)
            {
                var data = await connection.QueryAsync("select * from Loan where BankUserId = @BankUserId AND Amount > 0" , new { BankUserId = userId });
                if (data == null) return NotFound();
                return Ok(data);
            }
        }


    }
}
