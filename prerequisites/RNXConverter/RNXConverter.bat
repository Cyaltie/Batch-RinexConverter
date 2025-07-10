@echo off & setlocal enableextensions enabledelayedexpansion
::
cls
(set \n=^
%=This is Mandatory Space=%
)
:: Get the station list
echo;
set /p "leica=Leica site/s (psss):"
echo;
set /p "trimble=Trimble site/s (PSSS):"
::
:: Get the date
echo;
set /p "sdate=Start date (dd mm yyyy): "
echo;
set /p "edate=End date (dd mm yyyy): "
set "sy=%sdate:~6,4%"
set "sm=%sdate:~3,2%"
set "sd=%sdate:~0,2%"
set "ey=%edate:~6,4%"
set "em=%edate:~3,2%"
set "ed=%edate:~0,2%"
::
:: Get the time of observation
echo;
set /p "stime=UTC start time (hhmm, 24H): "
echo;
set /p "etime=UTC end time (hhmm, 24H): "
set "shr=%stime:~0,2%"
set "smn=%stime:~2,2%"
set "ehr=%etime:~0,2%"
set "emn=%etime:~2,2%"
::
:: Get the logging interval
echo;
set /p "int=Logging interval: "
::
:: Get the RINEX version
echo;
set /p "v=RINEX version (2/3): "
::
:: Get the navigation files
echo;
set /p "n=Navigation files (y/n): "
::
:: Get the RINEX type
echo;
set /p "h=Hatanaka/compressed RINEX (y/n): "
::
echo !\n!!\n!Convert data from %leica% and %trimble% to RINEX version %v% !\n!at logging interval %int%s from %sd%.%sm%.%sy% to %ed%.%em%.%ey% at %shr% %smn% to %ehr% %emn% !\n!with %n% nav file and %h% Hatanaka!\n! 
pause
::
:: Navigation file types
set "ntype=n g f l q c j i h" 
:: 
:: Month variables
set x[1]=31
set x[2]=28
set x[3]=31
set x[4]=30
set x[5]=31
set x[6]=30
set x[7]=31
set x[8]=31
set x[9]=30
set x[10]=31
set x[11]=30
set x[12]=31
::
:: Date/Time variables
set hr[0]=a
set hr[1]=b
set hr[2]=c
set hr[3]=d
set hr[4]=e
set hr[5]=f
set hr[6]=g
set hr[7]=h
set hr[8]=i
set hr[9]=j
set hr[10]=k
set hr[11]=l
set hr[12]=m
set hr[13]=n
set hr[14]=o
set hr[15]=p
set hr[16]=q
set hr[17]=r
set hr[18]=s
set hr[19]=t
set hr[20]=u
set hr[21]=v
set hr[22]=w
set hr[23]=x
::
:: Remove leading zeroes in preparation for computation
if %sm% lss 10 (set sm=%sm:~-1%)
if %sd% lss 10 (set sd=%sd:~-1%)
if %em% lss 10 (set em=%em:~-1%)
if %ed% lss 10 (set ed=%ed:~-1%)
if %shr% lss 10 (set shr=%shr:~-1%)
if %smn% lss 10 (set smn=%smn:~-1%)
if %ehr% lss 10 (set ehr=%ehr:~-1%)
if %emn% lss 10 (set emn=%emn:~-1%)
::
:: Call the day ordinal number subroutine
call :JDdayNumber %sd% %sm% %sy% DOY1
::
:: Call the day ordinal number subroutine
call :JDdayNumber %ed% %em% %ey% DOY2
::
for /l %%g in (%DOY1%,1,%DOY2%+1) do (
::
:: Copy and convert files for Leica sites
    for %%p in (%leica%) do (
	    echo %%p %%g
		set "DOY=%%g"
		set "site=%%p"
		
		call :CopyFiles %sy% %sm% %sd% %site% %DOY%
	    call :Raw2RNX %sy% %sm% %sd% %DOY% %site% %int% %v% %ntype% %n% %h%  
	)
	::
	:: Copy and convert files for Trimble sites
	for %%p in (%trimble%) do (
        set "DOY=%%g"
		set "site=%%p"
	    
   		call :CopyFiles %sy% %sm% %sd% %site% %DOY%
		call :Raw2RNX2 %sy% %sm% %sd% %DOY% %site% %int% %v% %ntype% %n% %h%
	)
	set /a sd+=1
)
echo !\n!!\n!Conversion completed
pause
::
endlocal & goto :EOF
::
:: ============================================================
:: Subroutine: Copy needed files for processing
:CopyFiles year month day site DOY
setlocal enableextensions enabledelayedexpansion
::
set "DOY2=0000%DOY%"
set "DOY3=%DOY2:~-3%"
::
set "sm2=00%sm%"
set "sd2=00%sd%"
set "sm3=%sm2:~-2%"
set "sd3=%sd2:~-2%"
::
set /a "i=%shr%"
if %emn% gtr 0 (
   set /a "j=%ehr%"
) else (
   set /a "j=%ehr%-1"
)
::
cls
::echo %i% %j%
::
for /l %%k in (%i%,1,%j%) do (
::   echo !hr[%%k]! %%k 
   echo !\n!!\n!Copying raw data...   
   if exist \\192.168.0.15\data\Raw_Data\%sy%\%sm3%\%sd3%\%site%\%site%%DOY3%!hr[%%k]!.*.zip (
      robocopy \\192.168.0.15\data\Raw_Data\%sy%\%sm3%\%sd3%\%site%\ C:\RNXConverter\Input\ %site%%DOY3%!hr[%%k]!.*.zip 
      7z e -r -aoa -oC:\RNXConverter\Input\Raw\ C:\RNXConverter\Input\%site%%DOY3%!hr[%%k]!.*.zip 
      del C:\RNXConverter\Input\%site%%DOY3%!hr[%%k]!.*.zip
   ) else (
      echo !\n!!\n!Moving to next site
   )
)
::
echo No more files to copy
::
endlocal & goto :EOF 
::
:: ============================================================
:: Subroutine: Convert MDB to RINEX 
:Raw2RNX year month day DOY site int ver navtype nav hat
setlocal enableextensions enabledelayedexpansion
::
set "DOY2=0000%DOY%"
set "DOY3=%DOY2:~-3%"
::
set "yr=%sy:~-2%"
::
set "sm2=00%sm%"
set "sm3=%sm2:~-2%"
::
set "sd2=00%sd%"
set "sd3=%sd2:~-2%"
::
set "source=C:\RNXConverter\Input\Raw\"
set "out=C:\RNXConverter\Output\"
set "home=C:\RNXConverter\"
::
cls
::echo %site% %DOY3% %sy% 
:: 
if exist %source%%site%%DOY3%*.m* (
   if "%v%"=="2" (
      echo !\n!!\n!Converting to RINEX 2
	  call mdb2rnx2.bat %source% %site%%DOY3%*.m* %out%
	  echo RINEX 2 done
   ) else (
      echo !\n!!\n!Converting to RINEX 3
      call mdb2rnx3.bat %source% %site%%DOY3%*.m* %out%
	  echo RINEX 3 done
   )
) else (
    echo !\n!!\n!No raw data to convert
)
:: 
cls
echo !\n!!\n!Concatenating the Rinex observation files...
gfzrnx -finp %out%%site%%DOY3%***.%yr%o -fout %out%Daily\%site%%DOY3%0.%yr%o -smp %int% -q -kv
::	
echo !\n!!\n!Fixing the header entries...
gfzrnx -finp %out%Daily\%site%%DOY3%0.%yr%o -fout %out%Edit\%site%%DOY3%0.%yr%o -crux %home%pagenetHDR.txt -hded -q
::
cls
if "%n%"=="y" (
   echo !\n!!\n!Working on the navigation files...
   for %%t in (%ntype%) do (
::      echo %site%%DOY3%***.%yr%%%t	  
      if exist %out%%site%%DOY3%***.%yr%%%t (
         gfzrnx -finp %out%%site%%DOY3%***.%yr%%%t -fout %out%Edit\%site%%DOY3%0.%yr%%%t -q -smp %int%
         robocopy %out%Edit\ %out%Final\ %site%%DOY3%0.%yr%*
      ) else (
         echo !\n!!\n!Navigation file of type %%t does not exist
      )
   )
) else (
   echo !\n!!\n!No navigation files included
)
::
cls
if "%h%"=="y" (
   echo !\n!!\n!Converting to Hatanaka...
   gfzrnx -finp %out%Edit\%site%%DOY3%0.%yr%o | rnx2crx > %out%Final\%site%%DOY3%0.%yr%d
   del %out%Final\%site%%DOY3%0.%yr%o
   echo !\n!!\n!Zipping files...
   7z a %out%Zip\%site%%DOY3%0.%yr%d.zip %out%Final\%site%%DOY3%0.%yr%*
) else (
   robocopy %out%Edit\ %out%Final\ %site%%DOY3%0.%yr%o
   echo !\n!!\n!No Hatanaka files included. Zipping files...
   7z a %out%Zip\%site%%DOY3%0.%yr%o.zip %out%Final\%site%%DOY3%0.%yr%*
)
::
echo !\n!!\n!Last minute housekeeping...
del %out%%site%%DOY3%***.%yr%*
del %out%Daily\%site%%DOY3%0.%yr%*
del %out%Edit\%site%%DOY3%0.%yr%*
::del %out%Final\%site%%DOY3%0.%yr%*
del %source%%site%%DOY3%*.m*
::
endlocal & goto :EOF 
::
:: ============================================================
:: Subroutine: Copy needed files for processing
:Raw2RNX2 year month day DOY site int ver navtype nav hat
setlocal enableextensions enabledelayedexpansion
::
set "DOY2=0000%DOY%"
set "DOY3=%DOY2:~-3%"
::
set "yr=%sy:~-2%"
::
set "sm2=00%sm%"
set "sm3=%sm2:~-2%"
::
set "sd2=00%sd%"
set "sd3=%sd2:~-2%"
::
set "source=C:\RNXConverter\Input\Raw\"
set "out=C:\RNXConverter\Output\"
set "home=C:\RNXConverter\"
::
set /a "i=%shr%"
if %emn% gtr 0 (
   set /a "j=%ehr%+1"
) else (
   set /a "j=%ehr%-1"
)
::
::echo %i% %j%
::
cls
for /l %%k in (%i%,1,%j%) do (
::   echo !hr[%%k]! %%k 
::   echo %source%%site%%DOY3%!hr[%%k]!.T02   
   if exist %source%%site%%DOY3%!hr[%%k]!.T02 (
      echo !\n!!\n!Converting T02 to RINEX
	  if "%v%"=="2" (
	     echo !\n!!\n!Converting to RINEX 2 %source%%site%%DOY3%!hr[%%k]!.T02 %out%
		 convertToRINEX %source%%site%%DOY3%!hr[%%k]!.T02 -v 2.11 -p %out%
		 ) else (
		 echo !\n!!\n!Converting to RINEX 3 %source%%site%%DOY3%!hr[%%k]!.T02 %out%
		 convertToRINEX %source%%site%%DOY3%!hr[%%k]!.T02 -v 3.02 -p %out%
		 )
   ) else (
      echo !\n!!\n!Moving to next site
   )
)
::
::echo %site% %DOY3% %sy% 
:: 
cls
echo !\n!!\n!Concatenating the Rinex observation files...
gfzrnx -finp %out%%site%%DOY3%***.%yr%o -fout %out%Daily\%site%%DOY3%0.%yr%o -smp %int% -q -kv
::	
echo !\n!!\n!Fixing the header entries...
gfzrnx -finp %out%Daily\%site%%DOY3%0.%yr%o -fout %out%Edit\%site%%DOY3%0.%yr%o -crux %home%pagenetHDR.txt -hded -q
::
cls
if "%n%"=="y" (
   echo !\n!!\n!Working on the navigation files...
   for %%t in (%ntype%) do (
::      echo %site%%DOY3%***.%yr%%%t	  
      if exist %out%%site%%DOY3%***.%yr%%%t (
         gfzrnx -finp %out%%site%%DOY3%***.%yr%%%t -fout %out%Edit\%site%%DOY3%0.%yr%%%t -q -smp %int%
         robocopy %out%Edit\ %out%Final\ %site%%DOY3%0.%yr%*
      ) else (
         echo !\n!!\n!Navigation file of type %%t does not exist
      )
   )
) else (
   echo !\n!!\n!No navigation files included
)
::
cls
if "%h%"=="y" (
   echo !\n!!\n!Converting to Hatanaka...
   gfzrnx -finp %out%Edit\%site%%DOY3%0.%yr%o | rnx2crx > %out%Final\%site%%DOY3%0.%yr%d
   del %out%Final\%site%%DOY3%0.%yr%o
   echo !\n!!\n!Zipping files...
   7z a %out%Zip\%site%%DOY3%0.%yr%d.zip %out%Final\%site%%DOY3%0.%yr%*
) else (
   robocopy %out%Edit\ %out%Final\ %site%%DOY3%0.%yr%o
   echo !\n!!\n!No Hatanaka files included. Zipping files...
   7z a %out%Zip\%site%%DOY3%0.%yr%o.zip %out%Final\%site%%DOY3%0.%yr%*
)
::
echo !\n!!\n!Last minute housekeeping...
del %out%%site%%DOY3%***.%yr%*
del %out%Daily\%site%%DOY3%0.%yr%*
del %out%Edit\%site%%DOY3%0.%yr%*
::del %out%Final\%site%%DOY3%0.%yr%*
del %source%%site%%DOY3%*.T02
::
endlocal & goto :EOF 
::
:: ============================================================
:: Subroutine: Calculate a day's ordinal number within the year
:JDdayNumber day month year return_
setlocal enableextensions enabledelayedexpansion
::
:: Get the date
set day=%~1
set month=%~2
set year=%~3
::
if %2 LEQ 2 (
  set /a f=%1-1+31*^(%2-1^)
  ) else (
  set /a a=%3
  set /a b=!a!/4-!a!/100+!a!/400
  set /a c=^(!a!-1^)/4-^(!a!-1^)/100+^(!a!-1^)/400
  set /a s=!b!-!c!
  set /a f=%1+^(153*^(%2-3^)+2^)/5+58+!s!
  )
set /a return_=%f%+1
::set /a return_=%f%-1
endlocal & set "%4=%return_%" & goto :EOF