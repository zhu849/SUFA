
int buzzer = 8; // buzzer pin
int trigPin = 12; //ultrasound trig Pin
int echoPin = 11; //ultrasound echo Pin
long duration, cm;

// NULL = None, 1 = green, 2 = red 
int traffic_light;
// store recive signal
char sign;

void setup() {
  Serial.begin (9600);             // Serial Port begin
  // set input & output pin 
  pinMode(trigPin, OUTPUT);  
  pinMode(echoPin, INPUT);
  pinMode(buzzer, OUTPUT);
  traffic_light = 0;
}

void check_pass(int cm){
  //green light and success across
  //serial print '8' mean success
  if(traffic_light == 1 && cm < 50){
    Serial.println('8');
    tone(buzzer, 500);
    delay(500); 
    noTone(buzzer);
    delay(200); 
  }
  //red light but across
  //serial print '9' mean failure
  else if(traffic_light == 2 && cm < 50){
    Serial.println('9');
    tone(buzzer, 100);
    delay(1500); 
    noTone(buzzer);
    delay(200); 
  }
}

void check_status(char sign){
  //Serial.println(sign);
  if(sign == '1'){
    traffic_light = 1;
    //Serial.println("Now status is green.");
  }
  else if(sign == '2'){
    traffic_light = 2;
    //Serial.println("Now status is red.");
  }
}

void loop()
{
  Serial.println('0');
  sign = 0;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(5);
  digitalWrite(trigPin, HIGH);  // 給 Trig 高電位，持續 10微秒
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  pinMode(echoPin, INPUT); // 讀取 echo 的電位
  duration = pulseIn(echoPin, HIGH); // 收到高電位時的時間
  
  cm = (duration/2) / 29.1;  // 將時間換算成距離 cm 或 inch  
  // everyloop check if anything fly over ultrasound sensor
  check_pass(cm);
  
  // everyloop check if any string receive from serial
  if(Serial.available() > 0) {
    while (Serial.available()){
      char c = Serial.read();
      if(c != '\n')
        sign = c;
      delay(5);
    }
    delay(10);
  }
  check_status(sign);
  //print out
  /*
  Serial.print("Traffic light: ");
  Serial.print(traffic_light);
  Serial.println();
  Serial.print("Distance : "); 
  Serial.print(cm);
  Serial.print("cm");
  Serial.println();
  */
  delay(500);
}
