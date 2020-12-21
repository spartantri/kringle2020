# 2) Investigate S3 Bucket
Difficulty: 1/5

When you unwrap the over-wrapped file, what text string is inside the package? Talk to Shinny Upatree in front of the castle for hints on this challenge.

ANSWER: North Pole: The Frostiest Place on Earth

## Starting the challenge
Click on the challenge terminal and it will pop-up on the scree and will show the following banner:
```
Can you help me? Santa has been experimenting with new wrapping technology, and
we've run into a ribbon-curling nightmare!
We store our essential data assets in the cloud, and what a joy it's been!
Except I don't remember where, and the Wrapper3000 is on the fritz!
Can you find the missing package, and unwrap it all the way?
Hints: Use the file command to identify a file type. You can also examine
tool help using the man command. Search all man pages for a string such as
a file extension using the apropos command.
To see this help again, run cat /etc/motd.
elf@098428dd9488:~$
```
## Get the pakcage
The bucket finder script needs a word list so we add wraper3000 as per the description on the banner and we execute the script
```
elf@098428dd9488:~$ echo "wrapper3000" >>bucket_finder/wordlist 
elf@098428dd9488:~$ bucket_finder.rb -r us -d bucket_finder/wordlist -l log.txt
http://s3.amazonaws.com/kringlecastle
Bucket found but access denied: kringlecastle
http://s3.amazonaws.com/wrapper
Bucket found but access denied: wrapper
http://s3.amazonaws.com/santa
Bucket santa redirects to: santa.s3.amazonaws.com
http://santa.s3.amazonaws.com/
        Bucket found but access denied: santa
http://s3.amazonaws.com/wrapper3000
Bucket Found: wrapper3000 ( http://s3.amazonaws.com/wrapper3000 )
        <Downloaded> http://s3.amazonaws.com/wrapper3000/package
```
The script will create a directory with the same name as the bucket and downloads the content  into the directory.
There is a single file in the directory and contains a base64 encoded payload.

## Unwarapping the package
The package file contains several layers of packaging, a simple base64 decode and unzip in cyberchef shows it contains a file named `package.txt.Z.xz.xxd.tar.bz2`

So let's unwrap it, we first do the base64 decode, then unzip then decompress bz2 and un tar the file
```
cat wrapper3000/package |base64 -d |gzip -d - |tar -jxf -
```
Now we have un-xxd the resulting file
```
cat package.txt.Z.xz.xxd |xxd -r -p > package.txt.Z.xz
```

## Cyberchef
http://icyberchef.com/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true)Unzip('',false)Bzip2_Decompress(false)Untar()From_Hexdump()Detect_File_Type(true,true,true,true,true,true,true)&input=VUVzREJBb0FBQUFBQUlBd2hGRWJSVDhhbndFQUFKOEJBQUFjQUJ3QWNHRmphMkZuWlM1MGVIUXVXaTU0ZWk1NGVHUXVkR0Z5TG1KNk1sVlVDUUFEb0JmS1g2QVh5bDkxZUFzQUFRVDJBUUFBQkJRQUFBQkNXbWc1TVVGWkpsTloya3RpdndBQkh2K1EzaEFTZ0dTbi8vQXZCeER3Zi94ZTBnUUFBQWd3QVZta1lSVEtlMVBWTTlVMGVrTWcycG9BQUFHZ1BVUFVHcWVoaENNU2dhQm9BRDFOTkFBQUF5RW1KcFI1UUdnMGJTUFUvVkEwZW85SWFIcUJreHcyWVpLMk5VQVNPZWdESXp3TVhNSEJDRkFDZ0lFdlEySnJnOFY1MHREamg2MVB0M1E4Q21ncEZGdW5jMUlwdWkrU3FzWUIwNE0vZ1dLS2MwVnMyRFhremVKbWlrdElOcWpvM0pqS0FBNGRMZ0x0UE4xNW9BRExlODB0bmZMR1hoSVdhSk1pRWVTWDk5MnV4b2RSSjZFQXpJRnpxU2JXdG5OcUNURURNTDlBSzdISFN6eXlCWUt3Q0ZCVkpoMTdUNjM2YTZZZ3lqWDBlRTBJc0NiamNCa1JQZ2tLejZxMG9rYjFzV2ljTWFreTJNZ3NxdzJuVW01YXlQSFVlSWt0bkJJdmtpVVd4WUVpUnM1bkZPTThNVGs4U2l0VjdsY3hPS3N0MlFlZFN4Wjg1MWNlRFFleHNMc0ozQzg5Wi9nUTZYbjZLQktxRnNLeVRrYXFPKzFGZ21JbXRIS29Ka01jdGQyQjlKa2N3dk1yK2hXSUVjSVFqQVpHaFNLWU5QeEhKRnFKM3QzMlZqZ24vT0dkUUppSUh2NHU1SXB3b1NHMGxzVitVRXNCQWg0RENnQUFBQUFBZ0RDRVVSdEZQeHFmQVFBQW53RUFBQndBR0FBQUFBQUFBQUFBQUtTQkFBQUFBSEJoWTJ0aFoyVXVkSGgwTGxvdWVIb3VlSGhrTG5SaGNpNWllakpWVkFVQUE2QVh5bDkxZUFzQUFRVDJBUUFBQkJRQUFBQlFTd1VHQUFBQUFBRUFBUUJpQUFBQTlRRUFBQUFB