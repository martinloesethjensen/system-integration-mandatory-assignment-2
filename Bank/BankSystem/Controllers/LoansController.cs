using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using BankSystem.Interfaces;
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
        public async Task<IActionResult> CreateLoan([FromBody] string value)
        {
            /*
             * Request will contain the BankUserIdand LoanAmount. 
             * A POST request will be made to the Loan Algorithm Functionwith an amount and the total account amount for that user
             * If the status code is 200, a loan record will be created
             * If the status code is 403 or similar, an error will be returned
             * The amount will be added to the Account of that user –if it is successfulof course.
             */
            return Ok();
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
