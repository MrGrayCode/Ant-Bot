/*
* Team ID : 117
* Author List : Ebey Abraham
* Filename : line_sensor.ino
* Theme : Antbot
* Functions : 
* Global Variables : pin1 -> analog pin for left sensor
                     pin2 -> analog pin for center sensor
                     pin3 -> analog pin for right sensor
                     left -> stores value of left sensor
                     right -> stores value of center sensor
                     center -> stores value of right sensor
                     thresh -> threshold of line sensor
*/
int pin1 = 0;
int pin2 = 1;
int pin3 = 2;
int left = 0;
int center = 0;
int right = 0;
int thresh = 140;

/*
* Function Name : lineSensor
* Input : NONE
* Output : prints the corresponding case according to the position of the line sensor
* Logic : read the values of the three pairs of sensors and accordingly choose the case to execute.
* Example Call : lineSensor()
*/
void lineSensor()
{
  left = analogRead(pin1);
  center = analogRead(pin2);
  right = analogRead(pin3);
  /*
  Serial.print(left);
  Serial.print(",");
  Serial.print(center);
  Serial.print(",");
  Serial.println(right);
  */
  
  if(left <= thresh && center <= thresh && right >= thresh) //soft right
  {
    Serial.println("1");
  }
  else if(left <= thresh && center >= thresh && right >= thresh) //soft right
  {
    Serial.println("2");
  }
  else if(left <= thresh && center >= thresh && right <= thresh) //straight
  {
    Serial.println("3");
  }
  else if(left >= thresh && center <= thresh && right <= thresh)  //soft left
  {
    Serial.println("4");
  }
  else if(left >= thresh && center >= thresh && right <= thresh)  //soft left
  {
    Serial.println("5");
  }
  else if(left >= thresh && center >= thresh && right >= thresh) //stop
  {
    Serial.println("6");
  }
}

void setup()
{  
 Serial.begin(9600);
}

void loop() 
{
  lineSensor();
  delay(10);
}
