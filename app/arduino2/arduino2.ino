//#include <SPI.h>

#include "DHT.h"
#include <SD.h>  
#include <TMRpcm.h> 

//DEFINES
#define SD_ChipSelectPin 53  //example uses hardware SS pin 53 on Mega2560
#define SPEAKER_PIN 46   //pino de saida para autofalante
#define DHTTYPE DHT11 // DHT 11
#define COMMMANDSIZE 5
#define PLAYLISTSIZE 12

//GLOBAL VARIABLES
int ledPin = 10;        //Porta a ser utilizada para ligar o led  
int LDRPin = A5;        //Porta analógica utilizada pelo LDR 
int DHT11Pin = 4;
int ledAirCondPin = 11;
int state = 0;         //valor fornecido pelo LDR 
int dhtvalue = 23;
String incoming = "";   // for incoming serial data

DHT dht(DHT11Pin, DHTTYPE);
TMRpcm tmrpcm;   // objeto de manipulacao de audio

String allsounds[PLAYLISTSIZE] = { "01_sozinho.wav", "02_voce_nao_me_ensinou.wav", "03_voce_e_linda.wav", "04_samba_de_verao.wav", 
                      "05_debaixo_dos_caracois.wav", "06_come_as_you_are.wav", "07_rapte_me_camaleoa.wav", "08_atras_da_verde_rosa.wav", 
                      "09_sampa.wav", "10_leaozinho.wav", "11_como_uma_onda.wav", "12_menino_do_rio.wav" };

String allWords[PLAYLISTSIZE] = { "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12" };

String allCommand[COMMMANDSIZE] = { "acende", "apaga", "pisca", "liga", "desliga" };


void setup() {
    Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
    pinMode(ledPin, OUTPUT);
    pinMode(ledAirCondPin, OUTPUT);
    dht.begin();

    //initializing audio devices
    tmrpcm.speakerPin = SPEAKER_PIN; 
    if (!SD.begin(SD_ChipSelectPin)) {  // inicializando o SDcard
        Serial.println("SD fail");
    } else {
        Serial.println("Initialization Done!"); 
    }
    tmrpcm.setVolume(5);

}

void loop() {

    // send data only when you receive data:
    if (Serial.available() > 0) {

        while (true) {
            // read the incoming byte:
            incoming = Serial.readString();  
            int command_index = indexOf(allCommand, incoming, COMMMANDSIZE);
            //int command_index = allCommand.indexOf(incoming);  
            int sound_index = -1;
 
            switch (command_index) {
                case 0 :
                    state = analogRead(LDRPin);
                    if (state > 800) {  
                        digitalWrite(ledPin, HIGH);
                        Serial.println("Acendendo"); 
                    }
                    break;
                case 1 :
                    digitalWrite(ledPin, LOW);
                    Serial.println("Apagando");
                    break;
                case 2 :
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
                case 3 :
                    float h = dht.readHumidity();
                    float t = dht.readTemperature();
                    // testa se retorno é valido, caso contrário algo está errado.
                    if (isnan(t) || isnan(h)) {
                        Serial.println("Failed to read from DHT");
                    } else {
                        Serial.print(t);  
                        if (t > 25) {
                            digitalWrite(ledAirCondPin, HIGH);
                            Serial.println("Ligando");
                        }
                    }
                    break;
                case 4 :
                    digitalWrite(ledAirCondPin, LOW);
                    Serial.println("Desligando");
                    break;        
                default:
                    sound_index = indexOf(allWords, incoming, PLAYLISTSIZE);
                    if (sound_index > -1) {
                        play_sound(allsounds[sound_index]); 
                    } else { 
                        Serial.println("UNKNOWN OPTION!!");
                    }
                break;
            }
        }
    }
}

void play_sound(String file) {
    tmrpcm.play(file); //the sound file "music" will play each time the arduino powers up, or is reset
}

int indexOf(String arrayString[], String word, int arraySize) {
  for (int i = 0; i < arraySize; i ++) {
    if (arrayString[i] == word) {
      return i;
    }
  }
  return -1;
}

