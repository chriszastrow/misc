//C# windows console program by Chris Zastrow.
//User input creates & modifies customer account & order records.
//Records are retrived & updated in a MySQL database where they are stored.
using System;
using MySql.Data.MySqlClient;

namespace CustomerOrders
{
    //Class Customer collects user input to construct customer records:
    class Customer
    {
        //Class Variables:
        public static string _customerName { get; set; }
        public static string _customerPhone { get; set; }
        public static string _customerAddress { get; set; }
        //Initialize new customer record:
        public Customer(string customerName, string customerPhone, string customerAddress)
        {
            _customerName = customerName;
            _customerPhone = customerPhone;
            _customerAddress = customerAddress;
        }
        //Print customer summary to console:
        public void Print()
        {
            Console.WriteLine("Customer Name: " + _customerName);
            Console.WriteLine("Phone Number: " + _customerPhone);
            Console.WriteLine("Delivery Address: " + _customerAddress);
        }
        //Accept console input to populate new customer record:
        public static Customer InputNewCustomer()
        {
            Console.WriteLine("Enter customer name:");
            string customerName = Console.ReadLine();
            Console.WriteLine("Enter customer phone number:");
            string customerPhone = Console.ReadLine();
            Console.WriteLine("Enter customer delivery address:");
            string customerAddress = Console.ReadLine();
            Customer newCustomer = new Customer(customerName, customerPhone, customerAddress);
            return newCustomer;
        }
    }
    //Class Database performs info transactions between client and database:
    class Database
    {
        //Class variables:
        public static string _recordNumber { get; set; }
        private static string mySqlString = "Server=_SQL_SERVER_;Database=_DB_NAME_;Uid=_USERNAME_;Pwd=_PASSWORD_;";
        //Write new customer record to database:
        public static void WriteCustomerRecord(
            string customerName, string customerPhone, string customerAddress)
        {
            MySqlConnection connection = new MySqlConnection(mySqlString);
            MySqlCommand cmd = connection.CreateCommand();
            connection.Open();
            cmd.CommandText = "INSERT INTO `customers` (`name`,`phone`,`address`) VALUES (@name,@phone,@address)";
            cmd.Parameters.AddWithValue("@name", customerName);
            cmd.Parameters.AddWithValue("@phone", customerPhone);
            cmd.Parameters.AddWithValue("@address", customerAddress);
            cmd.ExecuteNonQuery();
            connection.Close();
        }
        //Query database to check if customer record is existing:
        public static string ReadCustomerRecord(string customerName)
        {
            MySqlConnection connection = new MySqlConnection(mySqlString);
            MySqlCommand cmd = connection.CreateCommand();
            MySqlDataReader reader;
            connection.Open();
            cmd.CommandText = "SELECT `id` FROM `customers` WHERE `name`=@name";
            cmd.Parameters.AddWithValue("@name", customerName);
            reader = cmd.ExecuteReader();
            if (reader.Read() == true) { return reader.GetString("id"); } else { return null; }
        }
        //Write purchase order record to database:
        public static void WriteCustomerOrder(string orderType, string orderItem, string orderQuantity)
        {
            MySqlConnection connection = new MySqlConnection(mySqlString);
            MySqlCommand cmd = connection.CreateCommand();
            connection.Open();
            cmd.CommandText = "UPDATE `customers` SET `type`=@type, `item`=@item, `quantity`=@quantity WHERE `id`=@id";
            cmd.Parameters.AddWithValue("@id", Database._recordNumber);
            cmd.Parameters.AddWithValue("@type", orderType);
            cmd.Parameters.AddWithValue("@item", orderItem);
            cmd.Parameters.AddWithValue("@quantity", orderQuantity);
            cmd.ExecuteNonQuery();
            connection.Close();
        }
    }
    //Class Order collects user input to create customer order records:
    class Order
    {
        //Class variables:
        public static string _orderType { get; set; }
        public static string _orderItem { get; set; }
        public static string _orderQuantity { get; set; }
        //Initialize new order:
        public Order(string orderType, string orderItem, string orderQuantity)
        {
            _orderType = orderType;
            _orderItem = orderItem;
            _orderQuantity = orderQuantity;
        }
        //Print customer order to console:
        public void Print()
        {
            Console.WriteLine("Type of order: " + _orderType);
            Console.WriteLine("Item: " + _orderItem);
            Console.WriteLine("Quantity: " + _orderQuantity);
        }
        //Accept console input to populate new order:
        public static Order placeOrder()
        {
            Console.WriteLine("Enter the order type (Delivery, Pickup, or Catering):");
            string orderType = Console.ReadLine();
            Console.WriteLine("Enter the ordered item name:");
            string orderItem = Console.ReadLine();
            Console.WriteLine("Enter the ordered quantity of this item:");
            string orderQuantity = Console.ReadLine();
            Order newOrder = new Order(orderType, orderItem, orderQuantity);
            return newOrder;
        }
    }
    //Class Program is the Main program and misc functions:
    class Program
    {
        static void Main(string[] args)
        {
            //Request user input for customer name/phone/address:
            EnterCustomerInfo:
            Customer newCustomer = Customer.InputNewCustomer();
            Console.Clear();
            newCustomer.Print();
            Console.WriteLine("\n...Is the customer information correct?");
            if (!confirmInput()){ goto EnterCustomerInfo; }
            //Search for existing customer records, enter new record if none found, capture row id#:
            Database._recordNumber = Database.ReadCustomerRecord(Convert.ToString(Customer._customerName));
            if (Database._recordNumber != null)
            {
                Console.WriteLine("Existing customer record found, record #" + Database._recordNumber);
            }
            else
            {
                Console.WriteLine("Recording new customer to database...\n");
                Database.WriteCustomerRecord(Customer._customerName,Customer._customerPhone, Customer._customerAddress);
            }
            //Request user input for purchase order details & confirmation:
            EnterCustomerOrder:
            Order newOrder = Order.placeOrder();
            Console.Clear();
            newOrder.Print();
            Console.WriteLine("\n...Is the order information correct?");
            if (!confirmInput())
            {
                Console.Clear();
                goto EnterCustomerOrder;
            }
            else
            {
                Console.WriteLine("Recording new order to database...\n");
                Database.WriteCustomerOrder(Order._orderType, Order._orderItem, Order._orderQuantity);
                Console.Clear();
            }
            //Display full customer order info & ask if user wants to submit another order:
            Console.WriteLine("The order has been recorded as:\n\n");
            newCustomer.Print();
            newOrder.Print();
            Console.WriteLine("\n\n...Do you want to submit another order?");
            if (!confirmInput())
            {
                Console.Clear();
                Console.WriteLine("Press any key to exit.");
            }
            else
            {
                Console.Clear();
                goto EnterCustomerInfo;
            }
            Console.ReadKey();
        }
        //Function to request user Y/N confirmation:
        public static bool confirmInput()
        {
            Console.WriteLine("<Press 'Y' for Yes (or 'N' for No)>");
            ConsoleKeyInfo inputKey = Console.ReadKey();
            switch (inputKey.Key)
            {
                case ConsoleKey.Y:
                    Console.Clear();
                    return true;
                default:
                    Console.Clear();
                    return false;
            }
        }
    }
}
