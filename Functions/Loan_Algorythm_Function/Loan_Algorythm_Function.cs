using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using System.Net.Http;
using System.Net;

namespace LoanAlgorythm.Function
{
    public static class Loan_Algorythm_Function
    {
        [FunctionName("Loan_Algorythm_Function")]
        public static async Task<IActionResult> Run(
            [HttpTrigger(AuthorizationLevel.Anonymous, "post", Route = null)] HttpRequest req)
        {
            try
            {
                string requestBody = await new StreamReader(req.Body).ReadToEndAsync();
                dynamic data = JsonConvert.DeserializeObject(requestBody);
                double amount = data.loanAmount;
                double totalAmount = data.accountAmount;
                if (amount > totalAmount * 0.75) return new NotFoundResult(); //return new ForbidResult();
                return new OkObjectResult("success");
            }
            catch (Exception)
            {
                return new NotFoundResult();
            }
        }
    }
}
