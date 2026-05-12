# Accessibility

## WCAG 2.2 AA Conformance

The interactive mobility atlas targets WCAG 2.2 Level AA conformance.

## Implemented Measures

| Criterion | Implementation |
|-----------|---------------|
| 1.1.1 Non-text content | ARIA aria-label on figure container |
| 1.4.3 Contrast (minimum) | High-contrast palette (#003f5c to #ffa600); min 4.5:1 ratio |
| 1.4.11 Non-text contrast | Chart borders and axes meet 3:1 ratio |
| 2.1.1 Keyboard | Keyboard navigation handler in atlas HTML |
| 2.4.6 Headings and labels | Descriptive axis labels and figure title |
| 4.1.2 Name, Role, Value | role="figure" with aria-label |

## Colour Palette

The atlas uses a sequential palette with sufficient contrast for colour-blind users:

```
#003f5c -> #374c80 -> #7a5195 -> #bc5090 -> #ef5675 -> #ff764a -> #ffa600
```

This palette avoids red-green confusion and provides distinguishable steps in greyscale.

## Known Limitations

- Full WCAG 2.2 AA conformance for complex Plotly figures requires axe-core audit.
  Automated axe-core audit is integrated in the CI workflow.
- A static PNG fallback is provided for users who cannot access the interactive atlas.

## Testing

WCAG audit is performed via `axe-core` in the CI pipeline. Run locally with:

```bash
npx axe docs/figures/atlas.html --wcag2aa
```
