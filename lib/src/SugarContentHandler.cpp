#include <nsCExternalHandlerService.h>
#include <nsIFile.h>

#include "sugar-browser-chandler.h"
#include "SugarDownload.h"

#include "SugarContentHandler.h"

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
	nsCOMPtr<nsIFile> tmpFile;
	aLauncher->GetTargetFile(getter_AddRefs(tmpFile));
		
	aLauncher->SaveToDisk (tmpFile, PR_FALSE);

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
