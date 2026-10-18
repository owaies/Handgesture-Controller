# Gesture Presenter Manual Test Checklist

Use this checklist before publishing changes to the browser-based presenter. Run it in a current Chromium-based browser and at least one additional supported browser when practical.

## Camera and permissions

- [ ] Start the camera from a secure context (localhost or HTTPS) and confirm the live preview appears.
- [ ] Deny camera permission and confirm the interface explains how to recover without becoming stuck in a loading state.
- [ ] Stop the camera and confirm the camera indicator and preview reflect the stopped state.
- [ ] Test with no camera attached or with another application holding the camera.
- [ ] Reload after granting permission and confirm the app can start the camera again.

## Presentation controls

- [ ] Load a supported local presentation/PDF and confirm the first page renders.
- [ ] Move forward and backward using the visible controls.
- [ ] Verify navigation stays within the first and last pages.
- [ ] Test the configured hand gestures and confirm each action advances or reverses only as intended.
- [ ] Confirm manual controls remain usable when camera access is unavailable.

## Responsive and accessibility checks

- [ ] Check the main controls at a narrow mobile width and at a desktop width; verify they remain visible and operable.
- [ ] Navigate interactive controls with the keyboard and confirm focus remains visible.
- [ ] Confirm status and error messages are readable without relying only on color.
- [ ] Enable the operating system/browser reduced-motion preference and inspect transitions for unnecessary movement.
- [ ] Confirm camera denial, unsupported input, and rendering failures provide a clear recovery path.

Record browser, operating system, and the observed result for any failed item in the release notes or issue.
