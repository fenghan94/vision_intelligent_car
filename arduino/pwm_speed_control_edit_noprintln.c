//version2 control speed
#define LOW_SPEED 140
#define MIDDLE_SPEED 180
#define HIGH_SPEED 220
int l_motor_pwm = 5;
int r_motor_pwm = 6;

int l_pin1 = 4;   //IN1
int l_pin2 = 10;   //IN2
int r_pin3 = 7;   //IN3
int r_pin4 = 11;   //IN4

int command = 0;
int time = 50;

int max = LOW_SPEED;
int min = max - 40;
int speed = min;

void reset();
void sendCommand(int command, int time);

void lStop();
void lForward(int speed);
void lBack(int speed);
void rStop();
void rForward(int speed);
void rBack(int speed);

void stop();
void forward(int time);
void back(int time);
void turnLeft(int time);
void turnRight(int time);
void speedUp();
void speedDown();

void setup() {
  pinMode(l_motor_pwm, OUTPUT);
  pinMode(l_pin1, OUTPUT);
  pinMode(l_pin2, OUTPUT);
  pinMode(r_motor_pwm, OUTPUT);
  pinMode(r_pin3, OUTPUT);
  pinMode(r_pin4, OUTPUT);
  
  reset();
  
  Serial.begin(9600);   
  
  Serial.print("Enter keys -- w, s, q, a, d, 8, 5, 1, 2, 3 for drive control \n");
  Serial.print("w = Forward \n");
  Serial.print("s = Backward \n");
  Serial.print("q = Stop  \n");
  Serial.print("a = Turn Left  \n");
  Serial.print("d = Turn Right  \n");
  Serial.print("8 = Speed Up  \n");
  Serial.print("5 = Slow Down  \n");
  Serial.print("1 = Low Speed  \n");
  Serial.print("2 = Middle Speed  \n");
  Serial.print("3 = High Speed  \n");
}

void loop(){
  if (Serial.available() > 0) {
    command = Serial.read();
    sendCommand(command,time);
  }
  else{
    stop();
  }
}

void reset(){
  digitalWrite(l_motor_pwm, LOW);
  digitalWrite(l_pin1, LOW);
  digitalWrite(l_pin2, LOW);
  digitalWrite(r_motor_pwm, LOW);
  digitalWrite(r_pin3, LOW);
  digitalWrite(r_pin4, LOW);
}

void sendCommand(int command, int time){
  switch(command){
    case 'q': stop(); break;
    case 'w': forward(time); break;
    case 's': back(time); break;
    case 'a': turnLeft(time); break;
    case 'd': turnRight(time); break;
    case '8': speedUp(); break;
    case '5': speedDown(); break;
    case '1': max = LOW_SPEED; break;
    case '2': max = MIDDLE_SPEED; break;
    case '3': max = HIGH_SPEED; break;
  }
}

void lStop(){
  digitalWrite(l_motor_pwm, HIGH);
  digitalWrite(l_pin1, LOW);
  digitalWrite(l_pin2, LOW);
}
void lForward(int speed){
  analogWrite(l_motor_pwm, speed);
  digitalWrite(l_pin1, HIGH);
  digitalWrite(l_pin2, LOW);
}
void lBack(int speed){
  analogWrite(l_motor_pwm, speed);
  digitalWrite(l_pin1, LOW);
  digitalWrite(l_pin2, HIGH);
}
void rStop(){
  digitalWrite(r_motor_pwm, HIGH);
  digitalWrite(r_pin3, LOW);
  digitalWrite(r_pin4, LOW);
}
void rForward(int speed){
  analogWrite(r_motor_pwm, speed);
  digitalWrite(r_pin3, HIGH);
  digitalWrite(r_pin4, LOW);
}
void rBack(int speed){
  analogWrite(r_motor_pwm, speed);
  digitalWrite(r_pin3, LOW);
  digitalWrite(r_pin4, HIGH);
}

void stop(){
  lStop();
  rStop();
  speed = min;
  delay(time);
}
void forward(int time){
  speedUp();
  lForward(speed);
  rForward(speed);
  delay(time);
}
void back(int time){
  speedUp();
  lBack(speed);
  rBack(speed);
  delay(time);
}
void turnLeft(int time){
  rStop();
  lForward(speed);
  delay(time);
}
void turnRight(int time){
  lStop();
  rForward(speed);
  delay(time);
}
void speedUp(){
  if(speed<=max){
    speed+=10;
    Serial.println(speed);
  }
}
void speedDown(){
  if(speed>=min){
    speed-=10;
    Serial.println(speed);
  }
}
