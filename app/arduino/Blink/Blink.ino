String incoming = "";   // for incoming serial data
int ledPin = 5;

void setup() {
    Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
    pinMode(ledPin, OUTPUT);
}

void loop() {

    // send data only when you receive data:
    if (Serial.available() > 0) {

            while (true) {
                // read the incoming byte:
                incoming = Serial.readString();

                if (incoming == "acende") {
                    digitalWrite(ledPin, HIGH);
                } else if (incoming == "apaga") {
                    digitalWrite(ledPin, LOW);
                } else if (incoming == "pisca") {

                    digitalWrite(ledPin, HIGH);   // liga o LED
                    delay(300);                  // temporiza 1 segundo
                    digitalWrite(ledPin, LOW);    // desliga o LED
                    delay(300);    
                    digitalWrite(ledPin, HIGH);   // liga o LED
                    delay(300);                  // temporiza 1 segundo
                    digitalWrite(ledPin, LOW);    // desliga o LED
                    delay(300);
                    digitalWrite(ledPin, HIGH);   // liga o LED
                    delay(300);                  // temporiza 1 segundo
                    digitalWrite(ledPin, LOW);    // desliga o LED
                    delay(300);              // aguarda mais um segundo
                }
                
            }
    }
}
