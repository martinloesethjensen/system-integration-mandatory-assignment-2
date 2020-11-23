using Newtonsoft.Json;
using System.Net;
using System.Net.Http;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace BankSystem.Utils
{
    public class HTTP
    {
        public static async Task<HttpResponseMessage> PostRequest(string url, object content, CancellationToken cancellationToken)
        {
            using (var client = new HttpClient())
            using (var request = new HttpRequestMessage(HttpMethod.Post, url))
            {
                var json = JsonConvert.SerializeObject(content);
                using (var stringContent = new StringContent(json, Encoding.UTF8, "application/json"))
                {
                    request.Content = stringContent;

                    using (var response = await client
                        .SendAsync(request, HttpCompletionOption.ResponseHeadersRead, cancellationToken)
                        .ConfigureAwait(true))
                    {
                        response.EnsureSuccessStatusCode();
                        if (response.StatusCode == HttpStatusCode.OK) return response;
                        return null;
                    }
                }
            }
        }
    }
}
