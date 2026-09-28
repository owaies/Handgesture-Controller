# Browser Permission Notes

The application depends on browser access to the user's camera. Permission is requested by the browser and may be blocked at the site, tab, or operating-system level.

## Recovery steps

If the camera does not start:

1. Confirm the page is served from a context where camera access is permitted.
2. Check the browser's site permissions for camera access.
3. Verify no other application is holding the webcam exclusively.
4. Reload the page after changing permission.

The application should continue to present a clear status when camera access is unavailable rather than implying that gesture recognition is active.
