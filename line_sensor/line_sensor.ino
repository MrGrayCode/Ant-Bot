/*
* Team ID : 117
* Author List : Ebey Abraham
* Filename : line_sensor.ino
* Theme : Antbot
* Functions : lineSensor()
* Global Variables : left_pin -> analog pin for left sensor
                     center_pin -> analog pin for center sensor
                     right_pin -> analog pin for right sensor
                     left_val -> stores value of left sensor
                     right_val -> stores value of center sensor
                     center_val -> stores value of right sensor
                     thresh -> threshold of line sensor
                     kp ->
                     kd ->
*/

int left_pin = 2;
int center_pin = 1;
int right_pin = 0;
int left_val = 0;
int center_val = 0;
int right_val = 0;
int thresh = 165;
float position = 0;

/*
int setpoint = 500;
float error = 0;
float lastError = 0;
float kp = 0.02;
float kd = 0.0;

float motorSpeed = 0;
int rightBaseSpeed = 80;
int leftBaseSpeed = 80;
int rightMotorSpeed =0;
int leftMotorSpeed = 0;
*/
int checkPosition(int val)
{
  int res = 0;
  if(val>= thresh)
  {
    res = 1;
  }
  return res;
}

void printSensorValues()
{
  Serial.print(left_val);
  Serial.print(",");
  Serial.print(center_val);
  Serial.print(",");
  Serial.println(right_val);
}


/*
* Function Name : lineSensor
* Input : NONE
* Output : prints the corresponding case according to the position of the line sensor
* Logic : read the values of the three pairs of sensors and accordingly choose the case to execute.
* Example Call : lineSensor()
*/
void lineSensor()
{
  left_val = analogRead(left_pin);
  center_val = analogRead(center_pin);
  right_val = analogRead(right_pin);
  left_val = checkPosition(left_val);
  center_val = checkPosition(center_val);
  right_val = checkPosition(right_val);
  
  printSensorValues();
  
  if(left_val && center_val && right_val)
  {
    Serial.println("N");
  }
  else
  {
    position = (0*left_val + 500*center_val + 1000*right_val)/(left_val + center_val + right_val);
    Serial.println(position);
    /*
    error = setpoint - position;
    motorSpeed = kp * error + kd * (error - lastError);
    lastError = error;
    rightMotorSpeed = rightBaseSpeed + motorSpeed;
    leftMotorSpeed = leftBaseSpeed - motorSpeed;
    printMotorSpeeds();
    */
  }
}

void setup()
{  
 Serial.begin(9600);
}

void loop() 
{
  lineSensor();
  delay(100);
}
