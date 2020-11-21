using System;

namespace BankSystem.Utils
{
    public class TimeStamp
    {
        public static long GetDateTimeOffsetNowAsUnixTimeStampInSeconds() 
        {
            return DateTimeOffset.Now.ToUnixTimeSeconds();
        }
    }
}
