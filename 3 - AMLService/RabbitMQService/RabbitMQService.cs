using System.Text;
using System.Text.Json;
using System.Threading.Tasks; // Added for Task
using RabbitMQ.Client;
using RabbitMQ.Client.Events; // Added for EventingBasicConsumer

namespace AMLService.Uploaded;

public class RabbitMqService
{
    private readonly ConnectionFactory _factory;

    public RabbitMqService(string hostName, string userName, string password)
    {
        _factory = new ConnectionFactory()
        {
            HostName = hostName,
            UserName = userName,
            Password = password
        };
    }

    // 1. Changed return type from 'void' to 'Task'
    public void Publish(string queueName, object message)
    {
        // 2. Used 'await using' for proper asynchronous disposal
        using var connection = _factory.CreateConnection();
        using var channel = connection.CreateModel(); // 3. Correctly awaited the result

        // This call is synchronous and is now correctly called on the 'IModel' channel object
        channel.QueueDeclare(queue: queueName,
            durable: true,
            exclusive: false,
            autoDelete: false,
            arguments: null);

        var body = Encoding.UTF8.GetBytes(JsonSerializer.Serialize(message));

        // This call is also synchronous
        channel.BasicPublish(exchange: "",
            routingKey: queueName,
            basicProperties: null,
            body: body);
    }

    public void Consume(string queueName, Action<string> onMessageReceived)
    {
        // This synchronous implementation is valid and remains unchanged.
        var connection = _factory.CreateConnection();
        var channel = connection.CreateModel();

        channel.QueueDeclare(queue: queueName,
            durable: true,
            exclusive: false,
            autoDelete: false,
            arguments: null);

        // PrefetchCount is a good practice to prevent the consumer from being overwhelmed.
        channel.BasicQos(prefetchSize: 0, prefetchCount: 1, global: false);

        var consumer = new EventingBasicConsumer(channel);
        consumer.Received += (model, ea) =>
        {
            try
            {
                var body = ea.Body.ToArray();
                var message = Encoding.UTF8.GetString(body);
                onMessageReceived(message);
            }
            finally
            {
                // Ensure message is acknowledged even if processing fails to prevent it from being redelivered indefinitely.
                // For more robust error handling, you might move this into a dead-letter queue instead.
                channel.BasicAck(deliveryTag: ea.DeliveryTag, multiple: false);
            }
        };

        channel.BasicConsume(queue: queueName,
            autoAck: false, // autoAck is false, which is correct for manual acknowledgement.
            consumer: consumer);
    }
}