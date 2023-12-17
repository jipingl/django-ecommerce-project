// This is test publishable API key.
const stripe = Stripe("pk_test_51ONaoGJ7DBfLTFeg3v9lf9zmmYtYbnYexPeYw8WutlH7N76PsFhahq7xKjAB49GmkqgdFijpom9zkQbJfRrLTcDn00546zGvOv");
const clientSecret = document.getElementById('submit').getAttribute('data-secret');

// Create an instance of Elements.
let paymentElement;

initialize();
document.querySelector("#payment-form").addEventListener("submit", handleSubmit);

function initialize() {
    let elements = stripe.elements();

    const style = {
        base: {
            color: "#000",
            lineHeight: '2.4',
            fontSize: '16px'
        }
    };

    paymentElement = elements.create("card", {"style": style});
    paymentElement.mount("#card-element");

    paymentElement.on('change', function (event) {
        const displayError = document.getElementById('card-errors');
        if (event.error) {
            displayError.textContent = event.error.message;
            $('#card-errors').addClass('alert alert-info');
        } else {
            displayError.textContent = '';
            $('#card-errors').removeClass('alert alert-info');
        }
    });
}

function handleSubmit(e) {
    e.preventDefault()
    console.log(paymentElement)

    const customerName = document.getElementById("customer_name").value;
    const address = document.getElementById("address").value;
    const address2 = document.getElementById("address2").value;
    const postcode = document.getElementById("postcode").value;

    $.ajax({
        type: "POST",
        url: 'http://127.0.0.1:8000/order/add/',
        data: {
            order_key: clientSecret,
            full_name: customerName,
            address: address,
            postcode: postcode,
            csrfmiddlewaretoken: CSRF_TOKEN,
            action: "post",
        },
        success: function (json) {
            console.log(json.success)

            // Complete payment when the submit button is clicked
            stripe.confirmCardPayment(clientSecret, {
                payment_method: {
                    card: paymentElement,
                    billing_details: {
                        address: {
                            line1: address,
                            line2: address2
                        },
                        name: customerName
                    },
                }
            }).then(function (result) {
                if (result.error) {
                    console.log('payment error')
                    console.log(result.error.message);
                } else {
                    if (result.paymentIntent.status === 'succeeded') {
                        console.log('payment processed')
                        // There's a risk of the customer closing the window before callback
                        // execution. Set up a webhook or plugin to listen for the
                        // payment_intent.succeeded event that handles any business critical
                        // post-payment actions.
                        window.location.replace("http://127.0.0.1:8000/payment/order_placed/");
                    }
                }
            });

        },
        error: function (xhr, errmsg, err) {
        },
    });
}