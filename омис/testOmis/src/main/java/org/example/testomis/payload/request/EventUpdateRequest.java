package org.example.testomis.payload.request;

import jakarta.validation.constraints.NotBlank;
import org.example.testomis.model.enums.EventCategory;

public record EventUpdateRequest(
        @NotBlank
        String name,

        @NotBlank
        EventCategory category,

        @NotBlank
        String author,

        @NotBlank
        String start,

        @NotBlank
        String finish
) {
}
