#include <Servo.h>

Servo servo_motor;                                                               // creates a new instance of the Servo class
int Red[5] = {0, 7, 10, 13};                                                     // Pins where red light is connected
int Yellow[5] = {0, 6, 9, 12};                                                   // Pins where yellow light is connected
int Green[5] = {0, 5, 8, 11};                                                    // Pins where green light is connected
int Normal_cycle[5] = {0, 1, 2, 3};                                              // Default pattern i.e. Lanes 1 to 3
int GreenDelay = 2000, YellowDelay = 1500, next_lane, flag = 0, total_lanes = 3; // Basic parameters

void setup()
{
  Serial.begin(9600);
  servo_motor.attach(3); // Attaching motor signal pin at pin 3
  servo_motor.write(0);  // Keeping the motor at 0 degrees

  for (int i = 1; i < 1 + total_lanes; i++) // Basic Intialization
  {
    pinMode(Red[i], OUTPUT);
    pinMode(Yellow[i], OUTPUT);
    pinMode(Green[i], OUTPUT);
    digitalWrite(Red[i], HIGH);
    digitalWrite(Yellow[i], LOW);
    digitalWrite(Green[i], LOW);
  }
}

void ResetArray(int ResArr[]) // Used to reset the array to a default sequence
{
  for (int i = 1; i < 1 + total_lanes; i++)
  {
    ResArr[i] = i;
  }
}

void PythonArray(int valsRec[]) // Used to store the order of lanes recieve from the Python
{
  for (int i = 1; i < 1 + total_lanes; i++)
  {
    while (Serial.available() == 0)
    {
    }
    valsRec[i] = Serial.readStringUntil('\r').toInt();
  }
}

void Motor_Control() // Used to control the motor
{

  int current_position = 0; // Set the initial position of the servo motor to 0 degrees
  servo_motor.write(current_position);

  // Rotate the servo motor to 90 degrees in increments
  int target_position = 90;
  int increment = 1;
  while (current_position < target_position)
  {
    current_position += increment;
    servo_motor.write(current_position);
    delay(15);
  }

  Serial.println("Motor rotated to designated postion");
  while (Serial.readStringUntil('\r') != "Done") // Reading from Python, to see if Image detection is complete or not.
  {
  }
  // Rotate the servo motor to 180 degrees in increments
  target_position = 180;
  while (current_position < target_position)
  {
    current_position += increment;
    servo_motor.write(current_position);
    delay(15);
  }

  Serial.println("Motor rotated to designated postion");

  while (Serial.readStringUntil('\r') != "Done") // Reading from Python, to see if Image detection is complete or not.
  {
  }

  // Rotate the servo motor back to the initial position of 0 degrees in increments
  target_position = 0;
  while (current_position > target_position)
  {
    current_position -= increment;
    servo_motor.write(current_position);
    delay(15);
  }
  Serial.println("Motor rotated to designated postion");
}

void Lane_activation(int recieved_array[]) // It is used to intialize the traffic signal
{
  for (int i = 1; i < 1 + total_lanes; i++)
  {
    digitalWrite(Red[i], HIGH);
    digitalWrite(Yellow[i], LOW);
    digitalWrite(Green[i], LOW);
  }
  digitalWrite(Green[Normal_cycle[1]], HIGH);
  digitalWrite(Red[Normal_cycle[1]], LOW);
}

void Lane_rotation(int recieved_array[]) // This function is used to cycle between lanes
{
  for (int current_lane = 1; current_lane < 1 + total_lanes; current_lane++)
  {
    if (current_lane % total_lanes != 0) // Checks if the signal is on the last lane,  if it is not, then this set of code executes
    {
      flag = 0;
      next_lane = recieved_array[current_lane + 1];
      delay(GreenDelay);
      Transistion(recieved_array[current_lane], next_lane);
    }
    else // If it is on the last lane this set of code executes
    {
      Serial.println("Capture"); // Informs Python to start capturing
      while (Serial.readStringUntil('\r') != "Done")
      {
      }
      Motor_Control();                                // To start rotating the motor
      if (Serial.readStringUntil('\r').toInt() == 10) // Just to check if Python is sending list or other messages
      {
        flag = 1;
        int tmp_current_lane = recieved_array[current_lane];
        PythonArray(Normal_cycle);
        next_lane = recieved_array[1]; // Sets the next lane to the starting lane of the recieved sequence
        delay(GreenDelay);
        Transistion(tmp_current_lane, next_lane);
      }
      else
      {
        next_lane = recieved_array[1];
        delay(GreenDelay);
        Transistion(recieved_array[current_lane], 1);
      }
    }
  }
}

void Transistion(int i, int j) // This function is used to provide transition between signal switching
{
  if (i != j)
  {
    digitalWrite(Yellow[i], HIGH);
    digitalWrite(Yellow[j], HIGH);
    digitalWrite(Green[i], LOW);
    digitalWrite(Red[j], LOW);
    delay(YellowDelay);
    digitalWrite(Red[i], HIGH);
    digitalWrite(Yellow[i], LOW);
    digitalWrite(Yellow[j], LOW);
    digitalWrite(Green[j], HIGH);
  }
}

void loop()
{
  if (flag == 0) // To check if Python has sent list, else Resets to Deafult sequence 
  {
    ResetArray(Normal_cycle);
  }
  Lane_activation(Normal_cycle);
  Lane_rotation(Normal_cycle);
  // Loop completed
}
