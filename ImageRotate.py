import discord
import os
import Image
import io

client = discord.Client()

#check that the bot starts up
@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client)) #bot is running

#check each message
@client.event
async def on_message(message):
  if message.author == client.user: #if the message is from the bot then do nothing
    return

  if len(message.attachments) > 0: #if not self check if there is an attachment
    if message.attachments[0].content_type.startswith("image"): #check that the attachment is an image 
    
      command = message.content.lower() #normalize the case of the command
      attachment = message.attachments[0] #assign the first attachment as the image to be modified

      #check if the message, with an attachment, has an appropriate command
      if message.content == "$counterclockwise" or message.content == "$clockwise" or message.content == "$flip":
        imageBuffer = io.BytesIO(await discord.Attachment.read(attachment)) #wrap the image data in a byte buffer
        image = Image.open(imageBuffer) #image is opened using the byte buffer

        #image is now in memory and able to be modified
        #below is code to recognize the command and process the image acordingly
        #included is:
        #   rotate counter-clockwise
        #   rotate clockwise
        #   flip 

        #rotate the image counter-clockwise
        if command == "$counterclockwise":
          image_rotated = image.transpose(method=Image.ROTATE_90) #rotate the image counter-clockwise 90 degrees
          data = io.BytesIO() #new byte wrapper for the modified image
          image_rotated.save(data, format='png') #save the image to the byte wrapper
          data.seek(0) #ensure the pointer is at the start
          await message.channel.send(file=discord.File(data, "counterclockwise_rotated_image.png")) #send the image to the channel
        #rotate the image clockwise
        elif command == "$clockwise":
          image_rotated = image.transpose(method=Image.ROTATE_270) #rotate the image counter-clockwise 270 degrees (same as clockwise 90 degrees)
          data = io.BytesIO() #new byte wrapper for the modified image
          image_rotated.save(data, format='png') #save the image to the byte wrapper
          data.seek(0) #ensure the pointer is at the start
          await message.channel.send(file=discord.File(data, "clockwise_rotated_image.png")) #send the image to the channel
        #flip the image
        elif command == "$flip":
          image_rotated = image.transpose(method=Image.ROTATE_180) #rotate the image 180 degrees
          data = io.BytesIO() #new byte wrapper for the modified image
          image_rotated.save(data, format='png') #save the image to the byte wrapper
          data.seek(0) #ensure the pointer is at the start
          await message.channel.send(file=discord.File(data, "flipped_image.png")) #send the image to the channel
        
#line not needed if only using the above code in an existing bot
client.run(os.environ['token']) # "os.environ['token']" is an environment variable meaning it will be unique to your bot
