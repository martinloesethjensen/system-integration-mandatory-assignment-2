using BankSystem.Interfaces;
using Microsoft.Data.SqlClient;
using System;
using System.Data;
using System.Data.Common;

namespace BankSystem.Databases
{
    public class DatabaseStrategy : IDatabaseStrategy
    {
        private DbConnection _connection;

        public DbConnection Connection
        {
            get
            {
                if (_connection == null)
                {
                    _connection = new SqlConnection("Data Source=(localdb)\\MSSQLLocalDB;Initial Catalog=BankDb;Integrated Security=True;Connect Timeout=30;Encrypt=False;TrustServerCertificate=False;ApplicationIntent=ReadWrite;MultiSubnetFailover=False");
                    _connection.Open();
                }
                else if(_connection.State != ConnectionState.Open)
                {
                    _connection.Open();
                }
                return _connection;
            }
        }

        public void SeedDatabase()
        {
            throw new NotImplementedException();
        }
    }
}
