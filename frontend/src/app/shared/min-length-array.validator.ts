import { AbstractControl, ValidationErrors, ValidatorFn } from "@angular/forms";

export function minLengthArray(min: number): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    if (control.value.length >= min) {
      return null;
    }
    return { minLengthArray: true };
  };
}
