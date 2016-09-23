#include "DHT.h"
#include <SD.h>  
#include <TMRpcm.h> 

//DEFINES
#define SD_CHIP_SELECT_PIN 53  //example uses hardware SS pin 53 on Mega2560
#define SPEAKER_PIN 46         // 46 pino de saida para autofalante
#define DHT_TYPE DHT11         // DHT type: DHT11
#define COMMMAND_SIZE 5
#define PLAYLIST_SIZE 12

//GLOBAL VARIABLES        
int LDRPin = A5;        
int DHT11Pin = 4;
int ledAirCondPin = 9;
int ledPin = 10;

DHT dht(DHT11Pin, DHT_TYPE);
TMRpcm tmrpcm;   // objeto de manipulacao de audio

char* allSounds[PLAYLIST_SIZE] = { "01.wav", "02.wav", "03.wav", "04.wav", "05.wav", "06.wav", 
                                   "07.wav", "08.wav", "09.wav", "10.wav", "11.wav", "12.wav" };

String allWords[PLAYLIST_SIZE] = { "aquela", "triste", "mentira", "alegre", "calma", "rock", "prazer", "carnaval", "garoa", "beleza", "chateado", "12" };

String allCommand[COMMMAND_SIZE] = { "acende", "apaga", "pisca", "liga", "desliga" };


void setup() {
    Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
    pinMode(ledPin, OUTPUT);
    pinMode(ledAirCondPin, OUTPUT);
    dht.begin();

    //initializing audio devices
    tmrpcm.speakerPin = SPEAKER_PIN; 
    if (!SD.begin(SD_CHIP_SELECT_PIN)) {  // inicializando o SDcard
        Serial.println("SD fail");
    } else {
        Serial.println("Initialization Done!"); 
    }
    tmrpcm.setVolume(5);
    //tmrpcm.play("02.wav");

}

void loop() {

    /*while (true) {
      tmrpcm.play("01s.wav");
      Serial.println("tocando");
      delay(10000); 
    }*/

    String incoming = "";    // for incoming serial data
    while (true) {    //remover esse while?
        if (Serial.available() > 0) {

            incoming = Serial.readString();  
            int commandIndex = indexOf(allCommand, incoming, COMMMAND_SIZE);
            //Serial.println(commandIndex); 
            Serial.println("comando recebido: " + incoming); 
            
            switch (commandIndex) {
                case 0 : {
                    int state = 0;         //valor fornecido pelo LDR
                    state = analogRead(LDRPin); 
                    Serial.println("luminosidade: " + state); 
                    if (state > 800) {  
                        digitalWrite(ledPin, HIGH);
                        Serial.println("Acendendo lampada"); 
                    } else {
                        Serial.println("Luminosidade alta. Nao e necessario acender a lampada"); 
                    }
                    break;
                }
                case 1 :
                    digitalWrite(ledPin, LOW);
                    Serial.println("Apagando Lampada");
                    break;
                case 2 :
                    Serial.println("Piscando Lampada");
                    digitalWrite(ledPin, HIGH);   
                    delay(300);                  
                    digitalWrite(ledPin, LOW);    
                    delay(300);    
                    digitalWrite(ledPin, HIGH);   
                    delay(300);                  
                    digitalWrite(ledPin, LOW);    
                    delay(300);
                    digitalWrite(ledPin, HIGH);   
                    delay(300);                  
                    digitalWrite(ledPin, LOW);    
                    delay(300);              
                    break;
                case 3 : {
                    int dhtLimitValue = 23;
                    float h = dht.readHumidity();
                    float t = dht.readTemperature();
                    // testa se retorno é valido, caso contrário algo está errado.
                    if (isnan(t) || isnan(h)) {
                        Serial.println("Failed to read from DHT");
                    } else {
                        Serial.print("Temperatura: " + t );
                        Serial.print(248, DEC);   
                        Serial.print(" C\n");
                        if (t > dhtLimitValue) {
                            digitalWrite(ledAirCondPin, HIGH);
                            Serial.println("Ligando");
                        } else {
                            Serial.println("Temperatura Baixa. Nao e necessario ligar o ar condicionado");
                        }        
                    }
                    break;
                }
                case 4 :
                    digitalWrite(ledAirCondPin, LOW);
                    Serial.println("Desligando ar condicionado");
                    break;        
                default: {
                    int sound_index = -1; 
                    sound_index = indexOf(allWords, incoming, PLAYLIST_SIZE);
                    if (sound_index > -1) {
                        char* name; 
                        //name = allSounds[sound_index].c_str();;
                        name = allSounds[sound_index];
                        play_sound(name); 
                        Serial.println("Tocando musica: " + name);
                        //tmrpcm.play("01_sozinho.wav");
                    } else { 
                        Serial.println("UNKNOWN OPTION!!");
                    }
                    break;
                }
            }
        }
    }
    
}

void play_sound(char* file) {
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


int indexOf(char* arrayString[], String word, int arraySize) {
  for (int i = 0; i < arraySize; i ++) {
    if (arrayString[i] == word.c_str()) {
      return i;
    }
  }
  return -1;
}

/* FILES:

01.wav,   Sozinho   
02.wav,   Voce nao me ensinou a te esquecer
03.wav,   Voce e linda
04.wav,   Samba de verao 
05.wav,   debaixo_dos_caracois
06.wav,   Come_as_you_are 
07.wav,   Rapte_me_camaleoa 
08.wav,   Atras_da_verde_rosa 
09.wav,   Sampa 
10.wav,   leaozinho 
11.wav,   como_uma_onda 
12.wav,   menino_do_rio

*/
