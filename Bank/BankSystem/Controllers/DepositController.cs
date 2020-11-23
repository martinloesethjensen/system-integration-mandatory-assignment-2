using System;
using System.Net;
using System.Net.Http;
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
    public class DepositController : ControllerBase
    {
        private readonly IDatabaseStrategy _databaseContext;

        public DepositController(IDatabaseStrategy databaseContex)
        {
            _databaseContext = databaseContex;
        }

        // GET: api/<DepositController>
        [HttpGet("{bankUserId}")]
        public async Task<IActionResult> ListDeposits(int bankUserId)
        {
            /*
            * GETrequest that takes a BankUserId (/)
            * Returns a list of all the deposits that were made by that user (/)
            */

            using (var connection = _databaseContext.Connection)
            {
                var data = await connection.QueryAsync("select * from Deposit where BankUserId = @BankUserId", new { BankUserId = bankUserId });
                if (data == null) return NotFound();
                return Ok(data);
            }
        }

        // POST api/<DepositController>
        [HttpPost()]
        public async Task<IActionResult> AddDeposit([FromBody] DepositeRequest bodyPayload)
        {
            /*
             * Will receive a body with an amount and a BankUserId (/)
             * Amount deposited cannot be null or negative (/)
             * A deposit amount will first be sent to the interest rate function –the result will be saved in the database (/)
             * A record will be inserted in the deposits table as well (/)
             */

            if (bodyPayload.Amount <= 0) return Conflict("Amount cannot be null negative.");
            try
            {
                double interestRateFuncResponse = 0;
                HttpResponseMessage response = await HTTP.PostRequest("url", new { amount = bodyPayload.Amount }, CancellationToken.None ); // url is to be replaced
                if (response != null && response.StatusCode == HttpStatusCode.OK) interestRateFuncResponse = Convert.ToDouble(response.Content.ReadAsStringAsync());
                if (interestRateFuncResponse == 0) return NotFound("Interest rate function may be offline. Try again later.");
                DepositDto depositToInsert = new DepositDto(bodyPayload.BankUserId, TimeStamp.GetDateTimeOffsetNowAsUnixTimeStampInSeconds(), bodyPayload.Amount);

                using (var connection = _databaseContext.Connection)
                {
                    var result = await connection.ExecuteAsync("inser into Deposit (BankUserId,CreatedAt,Amount)" +
                                                               "values (@BankUserId,@CreatedAt,@Amount)", depositToInsert);
                    if (result != 1) NotFound("Deposit could not be added.");
                }

                return Ok("Deposit added.");
            }
            catch (Exception)
            {
                return NotFound();
            }
        }
    }
}
