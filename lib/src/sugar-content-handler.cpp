#include <stdio.h>

#include "sugar-content-handler.h"

GSugarContentHandler::GSugarContentHandler()
{

}

GSugarContentHandler::~GSugarContentHandler()
{

}

NS_IMPL_ISUPPORTS1(GSugarContentHandler, nsIHelperAppLauncherDialog)

NS_IMETHODIMP
GSugarContentHandler::Show (nsIHelperAppLauncher *aLauncher,
		       nsISupports *aContext,
		       PRUint32 aReason)
{

	return NS_OK;
}

NS_IMETHODIMP GSugarContentHandler::PromptForSaveToFile(
				    nsIHelperAppLauncher *aLauncher,			    
				    nsISupports *aWindowContext,
				    const PRUnichar *aDefaultFile,
				    const PRUnichar *aSuggestedFileExtension,
				    nsILocalFile **_retval)
{
	
	return NS_OK;
}
