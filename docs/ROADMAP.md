# Roadmap and Implementation Plan

## Completed in this package

1. Replaced the starter UI with a complete Radio Medical Record application.
2. Added all requested RMR fields from the nurse form.
3. Added bilingual English/Danish labels and bilingual feedback output.
4. Added upload endpoint for PDF, DOCX, TXT and scanned images.
5. Added OCR pathway for image/scanned reports using Tesseract.
6. Added professional PDF export without the word “Exam” in the title.
7. Added DMA-inspired visual theme and DMA public contact/reference information in the generated PDF.
8. Improved the clinical reasoning rules for examples like fast heartbeat after running.
9. Updated the run script to use `uvicorn app.main:app` and `npm run dev`.

## Next exam polish tasks

- Replace the placeholder DMA text mark with the official DMA logo only after permission is granted.
- Add more Promptfoo test cases for Danish inputs.
- Record a short demo video showing slow AI/file extraction operations.
- Add screenshots of the final UI to the report front page.
