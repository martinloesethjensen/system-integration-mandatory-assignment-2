using System.Collections.Generic;
using BankSystem.Interfaces;
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
        public IEnumerable<string> Get()
        {
            return new string[] { "value1", "value2" };
        }

        // GET api/<AccountsController>/5
        [HttpGet("{id}")]
        public string Get(int id)
        {
            return "value";
        }

        // POST api/<AccountsController>
        [HttpPost]
        public void Post([FromBody] string value)
        {
        }

        // PUT api/<AccountsController>/5
        [HttpPut("{id}")]
        public void Put(int id, [FromBody] string value)
        {
        }

        // DELETE api/<AccountsController>/5
        [HttpDelete("{id}")]
        public Delete(int id)
        {
        }
    }
}
