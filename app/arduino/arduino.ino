//include <dht11.h>

#include "DHT.h"

#define DHTTYPE DHT11 // DHT 11

String incoming = "";   // for incoming serial data
int ledPin = 10;        //Porta a ser utilizada para ligar o led  
int LDRPin = A5;        //Porta analógica utilizada pelo LDR 
int DHT11Pin = 4;
int ledAirCondPin = 11;
int state = 0;         //valor fornecido pelo LDR 
DHT dht(DHT11Pin, DHTTYPE);
int dhtvalue = 23;

void setup() {
    Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
    pinMode(ledPin, OUTPUT);
    pinMode(ledAirCondPin, OUTPUT);
    dht.begin();
}

void loop() {

    // send data only when you receive data:
    if (Serial.available() > 0) {

        while (true) {
            // read the incoming byte:
            incoming = Serial.readString();            
            /*switch (incoming) {
                case "acende":
                    state = analogRead(LDRPin);
                    if (state > 800) {  
                        digitalWrite(ledPin, HIGH);
                    }
                    break;
                case "apaga":
                    digitalWrite(ledPin, LOW);
                    break;
                case "pisca":
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
                    break;
                case "liga":
                    //float h = dht.readHumidity();
                    float t = dht.readTemperature();
                    // testa se retorno é valido, caso contrário algo está errado.
                    if (isnan(t) || isnan(h)) {
                        Serial.println("Failed to read from DHT");
                    } else {
                        if (t > 23) {
                            digitalWrite(ledAirCondPin, HIGH);
                        }
                    }
                    if (dhtvalue >= 23) {
                        digitalWrite(ledAirCondPin, HIGH);
                    }
                    break;
                case "desliga":
                    digitalWrite(ledAirCondPin, LOW);
                    break;        
                default: 
                  Serial.println("UNKNOWN OPTION!!");
                break;
            }*/
            
            if (incoming == "acende") {
                state = analogRead(LDRPin);
                if (state > 800) {  
                    digitalWrite(ledPin, HIGH);
                }
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
            } else if (incoming == "liga") {
                float h = dht.readHumidity();
                float t = dht.readTemperature();
                // testa se retorno é valido, caso contrário algo está errado.
                if (isnan(t) || isnan(h)) {
                    Serial.println("Failed to read from DHT");
                } else {
                    if (t > 23) {
                        digitalWrite(ledAirCondPin, HIGH);
                    }
                }
            } else if (incoming == "desliga") {
                digitalWrite(ledAirCondPin, LOW);
            } 
            
        }
    }
}
