int pin1 = 0;
int pin2 = 1;
int pin3 = 2;
int left = 0;
int center = 0;
int right = 0;
int thresh = 140;
char dir;

void setup()
{  
 Serial.begin(9600);
}

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

void loop() 
{
  lineSensor();
  delay(100);
}
